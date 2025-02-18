import asyncio
from crawl4ai import *
from pydantic_ai import Agent
 
from pydantic import BaseModel
 
from colorama import Fore
from dotenv import load_dotenv
import json

load_dotenv()  # take environment variables from .env.

class link(BaseModel):
    title: str
    href: str

class links_type(BaseModel):
    link_item: list[link]

async def get_content_and_links(url: str):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        return result
 

async def crawl_link_with_topic(url: str, topic: str, level: int):
    results = []
    result = await get_content_and_links(url)   
    jlinks = json.dumps(result.links["external"], ensure_ascii=False)
    print(Fore.GREEN, jlinks)
    
    link_filter_agent = Agent("openai:gpt-4o-mini",
                        system_prompt="""
                        you are a link selected agent, 
                        and you can filter out the links based on the provided topic,
                        only filter out links start with 'http://' or 'https://'
                        exclude all links start with 'file:'
                        """,
                        result_type=links_type
                    )
    filtered_links =  await link_filter_agent.run(f"links:{jlinks}, topic:{topic}")
    print(Fore.YELLOW,filtered_links.data)

    if level > 0:
        for link in filtered_links.data.link_item:
            print(Fore.BLUE, link)
            results = results + (await crawl_link_with_topic(link.href, topic, level - 1))

    results.append(f"{url}: {result.markdown}")
    return results

async def main():
    results = await crawl_link_with_topic("file://links.htm","貧血一般", 1)
    print(Fore.CYAN, results)
 
asyncio.run(main())