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

class check_item(BaseModel):
    check_date: str
    check_item: str
    ICD_10: str
    check_result: str

class report_output(BaseModel):
    patient_info: str
    checks: list[check_item]
    treatment: str
    summary: str
    conclusion: str
    followup: str
    hospital_name:str
    underwriting_assessment: str = Field(description="base on the information to suggest a underwriting decision with reasoning, include declined, approved or add loading")

def summary(context: str):
    @dataclass
    class medical_report:
        extracts: str
    
    #summary_model =  OllamaModel(
    #    model_name='deepseek-r1:1.5b',  
    #    base_url='http://localhost:11434/v1',  
    #)
 
    summary_agent = Agent(
        "openai:gpt-4o-mini",
        deps_type=medical_report
    )

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

def extractfile(pdf_file:str) -> str:
    @dataclass
    class deps:
        file_type: str
        file_path: str
        image_files: list[str]


    extraction_agent = Agent(
        model="openai:gpt-4o-mini", 
        result_retries=20, 
        deps_type = deps,
    )
        
    @extraction_agent.tool
    async def extract_image(ctx: RunContext[int], image_file) -> str:
        """
            extract image information from image_files
            for 通院 , try to extract the circled dates 
        """
        print(Fore.BLUE, f"extract from {image_file}\n")
        #result = "dummy"
        result = await getOCR(image_file)
        log(ctx.deps.file_path, image_file, result)
        return result

    @extraction_agent.tool
    async def extract_pdf2images(ctx: RunContext[int]) -> list[str]:
        """extract information from pdf file to images"""
        clear()
        print(Fore.RED, f"extract from {ctx.deps}")
        files = await extractpdf(ctx.deps.file_path)
        ctx.deps.image_files = files
        return files
    

    @extraction_agent.tool
    async def Diagnosis_mapping(ctx: RunContext, medical_finding: str):
        """if there is any Diagnosis,  use this function to map the icd 10 code"""
        print(Fore.GREEN, medical_finding)
        icd_agent = Agent(
            model="openai:gpt-4o-mini", 
            system_prompt="you are a icd mapper, and you can return the ICD code base on the impairment name"
        )
        result = await icd_agent.run(medical_finding)
        return result.data

    @extraction_agent.tool
    async def underwriting_assessment(ctx: RunContext):
        """base on the provided medical information for the underwriting assessment, include *reason and decision: [approved, declined, refer to human accessment]"""
        print(Fore.RED, ctx.messages)
        assessment_agent = Agent(
            model="openai:gpt-4o-mini", 
            system_prompt="You are an experience underwriter, you will base on the context provided to provide an underwriting decision, include *reason and decision: [approved, declined, refer to human accessment] ",
            deps_type=report_output
        )
        result = await assessment_agent.run("base on the provided context to provide underwriting assessment result and provide the reasons", deps=ctx.messages)
        print(Fore.RED, result)
        return result.data
    
    d = deps("pdf", pdf_file, [])
    result = extraction_agent.run_sync("""
                                        extract the information from pdf and get user information,
                                        if any medical information found, run the diagnosis_mapping, 
                                        then run the underwriting assessment 
                                       """, deps=d)
    print(Fore.GREEN, result)
    return result
    
def gen_report(context: str) -> report_output:
    #context = getall()
    report_agent = Agent(
        model="openai:gpt-4o-mini", 
        #model="openai:o3-mini",
        result_type=report_output
    )


       

    
    rpt = report_agent.run_sync(
        f"generate medical report from the context: {context}, and output need to be in English"
    )
    #print(Fore.GREEN, rpt.data, validate_hospital_name(rpt.data))
    return f"{rpt.data}, hospital verified: {validate_hospital_name(rpt.data)}"

def validate_hospital_name(hospital_name : str) -> str:
    if hospital_name == "SYNPHART SRINAKARIN HOSPITAL":
        return " (Verified)"
    else:
        return " (Not Verified)"
def write_file(content, filename):
    import codecs

    with codecs.open(f"{filename}", "w", "utf-8") as f:
        f.write(content)

def read_file(filename):
    import codecs
    with codecs.open(f"{filename}", "r", "utf-8") as f:
        return f.readlines()

def gen_html(report: str, filename: str):
    class htmloutput(BaseModel):
        html: str

    html_agent = Agent(
        model="openai:gpt-4o-mini", 
        result_type=htmloutput
    )

    html = html_agent.run_sync(f"generate the html base on the input data: {report}")
    #print(Fore.YELLOW, html.data.html)
    import codecs
    with codecs.open(f"{filename}.txt", "w", "utf-8") as f:
        f.write(report)

    with codecs.open(f"{filename}.html", "w", "utf-8") as f:
        f.write(html.data.html)
