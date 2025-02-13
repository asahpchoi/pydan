from dotenv import load_dotenv
load_dotenv()

import logfire
logfire.configure()

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
#from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
from colorama import Fore
from tools.tools import getOCR, extractpdf, getUserInfo  # Corrected import statement
from crawl4ai import AsyncWebCrawler
from pydantic_ai.usage import UsageLimits
from db import log, clear
from dataclasses import dataclass
from pydantic_ai.tools import ToolDefinition
from tools.agents import report_agent, report_output, assessment_agent, extraction_agent, summary_agent, extraction_deps, html_agent
import codecs


def summary(context: str):

    
    #summary_model =  OllamaModel(
    #    model_name='deepseek-r1:1.5b',  
    #    base_url='http://localhost:11434/v1',  
    #)
 


    @summary_agent.tool_plain
    async def getweb(url: str) -> str:    
        with AsyncWebCrawler() as crawler:
            result = crawler.arun(
                url=url,
            )
            return(result.markdown)
        
    result = summary_agent.run_sync(
        f"""you are a professional medical officer, try to collect the user information,
        you can complile a detail medical report from all the extractions in markdown format
        *ensure to keep all the key dates in the final report, e.g. check date, request date
        extract context: {context}"""
    )
    gen_report(result.data)
    #print(result.data)

def extractfile(pdf_file: str) -> str:

    @extraction_agent.tool
    async def extract_image(ctx: RunContext[int], image_file: str) -> str:
        """
            extact all the information from the image, 
            dont miss any dates and handwriting,
            focus on medical and checkup information
            all table information need to be presented in markdown
            output format should be in markdown
        """
        print(Fore.BLUE, f"extract from {image_file}\n")
        result = await getOCR(image_file)
        log(ctx.deps.file_path, image_file, result)
        return result

    @extraction_agent.tool
    async def extract_pdf2images(ctx: RunContext[int]) -> list[str]:
        """extract information from pdf file to images"""
        clear()
        print(Fore.RED, f"extract from {ctx.deps.file_path}")
        files = await extractpdf(ctx.deps.file_path)
        ctx.deps.image_files = files
        return files

    #@extraction_agent.tool
    async def Diagnosis_mapping(ctx: RunContext, medical_finding: str) -> str:
        """if there is any Diagnosis,  use this function to map the icd 10 code"""
        print(Fore.GREEN, medical_finding)
        icd_agent = Agent(
            model="openai:gpt-4o-mini",
            system_prompt="you are a icd mapper, and you can return the ICD code base on the impairment name"
        )
        result = await icd_agent.run(medical_finding)
        return result.data

    #@extraction_agent.tool
    async def underwriting_assessment(ctx: RunContext) -> str:
        """base on the provided medical information for the underwriting assessment, include *reason and decision: [approved, declined, refer to human accessment]"""
 

        result = await assessment_agent.run("base on the provided context to provide underwriting assessment result and provide the reasons", deps=ctx.messages)
 
        return result.data

    d = extraction_deps("pdf", pdf_file, [])
    result = extraction_agent.run_sync(
        """
        extract the information from pdf and get user information,
        if any medical information found, run the diagnosis_mapping,
        then run the underwriting assessment
        """,
        deps=d,
    )

    print(Fore.RED, result.data)
    
   
    with codecs.open(f"{pdf_file}.html.txt", "w", "utf-8") as f:
        f.write(result.data)
 
    return result.data
    
def gen_report(context: str, filename: str) -> report_output:
    rpt = report_agent.run_sync(
        f"generate medical report from the context: {context}, and output need to be in English"
    )

    html = html_agent.run_sync(f"generate the html base on the input data: {rpt}")

    with codecs.open(f"{filename}.html", "w", "utf-8") as f:
        f.write(rpt.data)
