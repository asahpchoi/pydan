from pydantic_ai import Agent, RunContext
from pydantic_ai.models.ollama import OllamaModel
from pydantic_ai.models.openai import OpenAIModel
import logfire
from colorama import Fore
from dotenv import load_dotenv
 
import os
from crawl4ai import AsyncWebCrawler

logfire.configure()
load_dotenv()  # take environment variables from .env.
 
ollama_model = OllamaModel(
    model_name='llama3-groq-tool-use',  
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

print(question)
agent = Agent(
    #model="openai:gpt-4o-mini", 
    #model='groq:llama-3.3-70b-versatile',
    model=mm_model,
    #model="google-gla:gemini-2.0-flash-exp",
    system_prompt="You are a underwriter who can provide profession advice to the team for the claim request form"
)

 
 
from crawl4ai import AsyncWebCrawler

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


result = agent.run_sync(
    question
#    "what is liver function that cannot have Life Cover"
#    #"who is ryan kim in fwd team?"
    )
print(Fore.BLUE, (result.data))
 



