from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
import logfire
from colorama import Fore
from tools.tools import getOCR, extractpdf
from crawl4ai import AsyncWebCrawler
from db import log
from config import question, mm_model # Import configurations from config.py

logfire.configure()


class Test(BaseModel):
    test_date: str
    reason: str
    test_result: str
    follow_up: str

class MedicalReport(BaseModel):
    dr_name: str
    dr_name_isVerified: bool

    check_result: list[Test]
    patient_info: str
    patient_height: int
    patient_weight: int
    lab_findings: str

class FileInfo(BaseModel):
    filename: str


agent = Agent(
    model="openai:gpt-4o-mini",
    #model='groq:llama-3.3-70b-versatile',
    #model=mm_model, # Use imported mm_model from config.py
    #ollama_model,
    #model="google-gla:gemini-2.0-flash-exp",
    deps_type=FileInfo,
    result_type=MedicalReport,
    result_retries=20,
)


async def verify_doctor_name(ctx: RunContext[str], dr_name) -> bool:
    """if any doctor name shown, verify doctor name"""
    print(Fore.CYAN, dr_name)
    return True


@agent.tool
async def get_medical_certificate(ctx: RunContext[int], image_file) -> str:
    """get medical report"""
    print(Fore.RED, image_file)
    print(Fore.RED, ctx)
    result = await getOCR(image_file)
    log(image_file, result)

    #print(Fore.RED, files, result)
    return result

@agent.tool
async def extract_pdf2images(ctx: RunContext[FileInfo], filename) -> []:
    """if user provide PDF, it will convert pdf to images"""


    files = await extractpdf(filename)
    print(Fore.YELLOW, files)
    return files


#@agent.tool
async def get_product_detail(ctx: RunContext[int]):
    # 初始化非同步網頁爬蟲
    """get product information"""
    async with AsyncWebCrawler(verbose=True) as crawler:
        # 爬取指定的 URL
        result = await crawler.arun(url="https://www.life.hsbc.co.uk/advisers/protection-advisers/pre-underwriting-guide/diabetes/")
        # 以 Markdown 格式顯示提取的內容
        print(result.markdown)
        return(result.markdown)

#@agent.tool
async def get_FWD_team(ctx: RunContext[int]):
    "get the name of FWD team"
    return "CEO: Phong, CDO: Ryan Kim"

#@agent.tool
async def get_patient_inf(ctx: RunContext):
    """get the patient information"""
    print(Fore.RED, ctx)
    return "Michelle Lau, 36, female"

@agent.system_prompt
def get_systemprompt():
    return "You are a underwriter who can provide profession advice to the team for the claim request form, final result should be in Chinese"

result = agent.run_sync(
    f"""prepare the medical certificate for an insurnace claim, you can get the information from the medical certificate
        , file in 'pdfs/p2.pdf'
        question: {question}
    """,

#    "what is liver function that cannot have Life Cover"
#    #"who is ryan kim in fwd team?"
    #usage_limits=UsageLimits(response_tokens_limit=20),
    )

print(Fore.BLUE,  (result.data))
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
import logfire
import json
from colorama import Fore
from dotenv import load_dotenv
from tools.tools import getOCR, extractpdf
import os
from crawl4ai import AsyncWebCrawler
from pydantic_ai.usage import UsageLimits
from db import log

logfire.configure()
load_dotenv()  # take environment variables from .env.
 
ollama_model = OllamaModel(
    model_name='deepseek-r1:1.5b',  
    base_url='http://localhost:11434/v1',  
)

ds_model = OpenAIModel(
    'deepseek-chat',
    base_url='https://api.deepseek.com',
    api_key=os.environ["DEEPSEEK_API_KEY"],
)

mm_model = OpenAIModel(
    "MiniMax-Text-01",
    base_url="https://api.minimaxi.chat/v1",
    api_key=os.environ["MINIMAX_API_KEY"]
)

#agent = Agent('google-gla:gemini-2.0-flash-exp')
#agent = Agent(model=ollama_model)
#agent = Agent(model=ds_model)

question = """
    Condition: Itchy and painful keloid
    Please confirm the exact date of onset of keloid.
    Please advise where did the keloid come from e.g. accident/injury details, date of accident/injury
    Please confirm the exact date of keloid starting to get itchy and painful
    Please advise if you have ever seen any other medical practitioner for keloid condition.
    Please confirm if Dr Lam is the first practitioner you have seen for keloid condition.
    Please confirm if any previous treatment has been done to treat keloid.  
    Condition: Viral warts
    Please confirm if this is the first time you have had warts. If not please provide date for previous condition.
    Please confirm the exact date of onset of symptoms (dd/mm/yyyy)? 
    Please advise if you have ever seen any other medical practitioner for warts condition.
    Please confirm if Dr Lam is the first practitioner you have seen for warts condition.
    Please confirm if any previous treatment has been done to treat warts e.g. Co2 or other cauterization.

"""
class Test(BaseModel):
    test_date: str
    reason: str
    test_result: str
    follow_up: str

class MedicalReport(BaseModel):
    dr_name: str
    dr_name_isVerified: bool
 
    check_result: list[Test]
    patient_info: str
    patient_height: int
    patient_weight: int
    lab_findings: str

class FileInfo(BaseModel):
    filename: str


 
agent = Agent(
    model="openai:gpt-4o-mini", 
    #model='groq:llama-3.3-70b-versatile',
    #model=mm_model,
    #ollama_model,
    #model="google-gla:gemini-2.0-flash-exp",
    deps_type=FileInfo, 
    result_type=MedicalReport,
    result_retries=20,
 
)

 
 
from crawl4ai import AsyncWebCrawler

@agent.tool
async def verify_doctor_name(ctx: RunContext[str], dr_name) -> bool: 
    """if any doctor name shown, verify doctor name"""
    print(Fore.CYAN, dr_name)
    return True


@agent.tool
async def get_medical_certificate(ctx: RunContext[int], image_file) -> str:
    """get medical report"""
    print(Fore.RED, image_file)
    print(Fore.RED, ctx)
    result = await getOCR(image_file)
    log(image_file, result)
    
    #print(Fore.RED, files, result)
    return result

@agent.tool
async def extract_pdf2images(ctx: RunContext[FileInfo], filename) -> []:
    """if user provide PDF, it will convert pdf to images"""
    
    
    files = await extractpdf(filename)
    print(Fore.YELLOW, files)
    return files


#@agent.tool
async def get_product_detail(ctx: RunContext[int]):
    # 初始化非同步網頁爬蟲
    """get product information"""
    async with AsyncWebCrawler(verbose=True) as crawler:
        # 爬取指定的 URL
        result = await crawler.arun(url="https://www.life.hsbc.co.uk/advisers/protection-advisers/pre-underwriting-guide/diabetes/")
        # 以 Markdown 格式顯示提取的內容
        print(result.markdown)
        return(result.markdown)

#@agent.tool
async def get_FWD_team(ctx: RunContext[int]):
    "get the name of FWD team"    
    return "CEO: Phong, CDO: Ryan Kim"

#@agent.tool
async def get_patient_inf(ctx: RunContext):
    """get the patient information"""
    print(Fore.RED, ctx)
    return "Michelle Lau, 36, female"

@agent.system_prompt
def get_systemprompt():
    return "You are a underwriter who can provide profession advice to the team for the claim request form, final result should be in Chinese"

result = agent.run_sync(
    """prepare the medical certificate for an insurnace claim, you can get the information from the medical certificate
        , file in 'pdfs/p2.pdf'
    """,
    
#    "what is liver function that cannot have Life Cover"
#    #"who is ryan kim in fwd team?"
    #usage_limits=UsageLimits(response_tokens_limit=20),
    )

print(Fore.BLUE,  (result.data))
