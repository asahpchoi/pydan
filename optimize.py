import sys
from process import extractfile, gen_report
from pydantic_ai import Agent
import codecs
from pydantic import BaseModel
from db import getall, getallrows
from colorama import Fore



class report_item(BaseModel):
    check_date: str
    description: str
    impact: str
    risk: str
#print(content)

class reports(BaseModel):
    items: list[report_item]


def get_enhanced_prompt(prompt: str) -> str:
    system_prompt = """
    You are a professional prompt engineer, 
    and you can rewrite and optimize the provided prompt to be more effective
    """

    prompt_agent = Agent(
        model="openai:gpt-4o-mini",
        system_prompt=system_prompt
    )

    result = prompt_agent.run_sync(prompt)
    return result.data

def get_report_items(page_number: int, content: str):
    assessment_agent = Agent(
        model="openai:gpt-4o-mini",
        system_prompt=get_enhanced_prompt("""
            you are a professional underwriter, 
            the report should be easy to read, 
            you can based on the content provided to generate a comphensive report
            find out those unusual finding, complication, family history and testing
            all the finding need to be translated to English
        """),
        result_type=reports
    )

    result = assessment_agent.run_sync(content)
    j_result = f"page_no: {page_number}: {result.data.model_dump_json()}"

    return j_result

def gen_report(content: str):
    prompt = get_enhanced_prompt("""
            you are a html programmer, 
            you can based on the content provided to generate an html report, no javascript allowed,
            all the page number and testing item should be in table format,
            the report need to be professional,
            and you need to include all the findings in all pages,
            no background color in table
            if the item in high risk, highlight in RED
            if the item have medium risk, highlight in BLUE
            in the report, add a toggle button to show or hide base on the risk
        """)

    html_agent = Agent(
        model="google-gla:gemini-2.0-flash-thinking-exp-01-21",
        system_prompt= prompt,
        deps_type=reports
    )

    html = html_agent.run_sync(f"generate html report based on the dependency info : {content}" )

    with codecs.open(f"optimized.html", "w", "utf-8") as f:
        f.write(html.data)

def get_summary_from_db():
    rows = getallrows()
    i = 1
    contents = ""
    for c in rows:
        print(c[0])
        content = get_report_items(i, c[0])
        contents = f"page{i}: {contents}\n{content}"
        i = i+1


#===============================================================================

with codecs.open(f"conso.txt", "r", "utf-8") as f:
    contents = f.readlines()
gen_report(contents)