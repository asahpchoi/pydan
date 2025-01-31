from dotenv import load_dotenv
load_dotenv()

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
import logfire
import json
from colorama import Fore
from tools.tools import getOCR, extractpdf  # Corrected import statement
import os
from crawl4ai import AsyncWebCrawler
from pydantic_ai.usage import UsageLimits
from db import log, clear, getall
from dataclasses import dataclass
from pydantic_ai.tools import ToolDefinition

class check_item(BaseModel):
    check_date: str
    check_item: str
    check_result: str

class report_output(BaseModel):
    patient_info: str
    checks: list[check_item]
    summary: str
    conclusion: str


def summary():
    @dataclass
    class medical_report:
        extracts: str
    
    summary_model =  OllamaModel(
        model_name='deepseek-r1:1.5b',  
        base_url='http://localhost:11434/v1',  
    )
 
    summary_agent = Agent(
        summary_model,
        deps_type=medical_report
    )

    context = getall() 

    result = summary_agent.run_sync(
        f"""you are a professional medical officer, 
        you can complile a detail medical report from all the extractions in markdown format
        *ensure to keep all the key dates in the final report, e.g. check date, request date
        extract context: {context}"""
    )
    print(result.data)

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
        """extract image information from image_files"""
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


    d = deps("pdf", pdf_file, [])
    result = extraction_agent.run_sync("extract the information from pdf", deps=d)
    print(Fore.GREEN, result)
    return result
    

def gen_report(context) -> report_output:
    #context = getall()
    report_agent = Agent(
        model="openai:gpt-4o-mini", 
        result_type=report_output
    )
    rpt = report_agent.run_sync(
        f"generate medical report from the context: {context}, output need to be in Chinese"
    )
    return rpt.data
    #print(Fore.BLUE, rpt.data)

def gen_html(report):
    html_agent = Agent(
        model="openai:gpt-4o-mini", 
     
    )
    html = html_agent.run_sync(f"generate the html base on the input data: {report}")
    print(Fore.YELLOW, html.data)
    import codecs

    with codecs.open("report.html", "w", "utf-8") as f:
        f.write(html.data)

