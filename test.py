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
from db import log, clear
from dataclasses import dataclass
from pydantic_ai.tools import ToolDefinition

load_dotenv()  # take environment variables from .env.

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


d = deps("pdf", "pdfs/p2.pdf", [])
extraction_agent.run_sync("extract the information from pdf", deps=d)