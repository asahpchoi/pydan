from dotenv import load_dotenv
load_dotenv()

import logfire
logfire.configure()

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
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
    summary: str
    conclusion: str
    hospital_name:str

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

    @summary_agent.tool
    async def get_User_Info(ctx: RunContext[int]) -> str:
        """ extract user information """
        userinfo = await get_User_Info("12345")
        print(Fore.YELLOW, userinfo)
        return userinfo


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
    


    d = deps("pdf", pdf_file, [])
    result = extraction_agent.run_sync("extract the information from pdf and get user information", deps=d)
    print(Fore.GREEN, result)
    return result
    
def gen_report(context: str) -> report_output:
    #context = getall()
    report_agent = Agent(
        #model="openai:gpt-4o-mini", 
        model="openai:o3-mini",
        result_type=report_output
    )
    rpt = report_agent.run_sync(
        f"generate medical report from the context: {context}, output need to be in English"
    )
    print(Fore.GREEN, rpt.data, validate_hospital_name(rpt.data))
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

    with codecs.open(f"{filename}.html", "w", "utf-8") as f:
        f.write(html.data.html)



