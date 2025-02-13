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
    crawl_agent = Agent("google-gla:gemini-2.0-flash-exp",
                            system_prompt="you are a link selected agent, and you can filter out the links based on the provided topics",
                            result_type=links_type
                        )
    jlinks = json.dumps(result.links, ensure_ascii=False)
 
    filtered_links =  await crawl_agent.run(f"links:{jlinks}, topic:{topic}")
    print(Fore.RED, f"links to crawl: {filtered_links.data.link_item.count(0)}")

    if level > 0:
        for link in filtered_links.data.link_item:
            print(Fore.BLUE, link)
            results = results + (await crawl_link_with_topic(link.href, topic, level - 1))

    results.append(f"{url}: {result.markdown}")
    return results

async def main():
    results = await crawl_link_with_topic("https://www.kanen.ncgm.go.jp/cont/010/c_gata.html","fatty liver", 1)
    print(results)
 
asyncio.run(main())