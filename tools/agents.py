
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


class htmloutput(BaseModel):
    html: str

@dataclass
class extraction_deps:
    file_type: str
    file_path: str
    image_files: list[str]

@dataclass
class medical_report:
    extracts: str

report_agent = Agent(
    model="openai:gpt-4o-mini", 
    #model="openai:o3-mini",
    result_type=report_output
)

assessment_agent = Agent(
    model="openai:gpt-4o-mini",
    system_prompt="You are an experience underwriter, you will base on the provided context to provide underwriting assessment result and provide the reasons",
    deps_type=report_output
)

extraction_agent = Agent(
    model="openai:gpt-4o-mini",
    result_retries=20,
    deps_type=extraction_deps,
)

summary_agent = Agent(
    "openai:gpt-4o-mini",
    deps_type=medical_report
)

html_agent = Agent(
    model="openai:gpt-4o-mini",
    result_type=htmloutput
)
