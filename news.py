url = 'https://www.fool.com/research/'

import asyncio
from crawl4ai import *

async def main():
    markdown = []

    async def get_text(url):
        result = await crawler.arun(
            url=url, 
        )
        result.markdown

    async with AsyncWebCrawler() as crawler:
        crawler_cfg = CrawlerRunConfig(
            exclude_external_links=True,          # No links outside primary domain
            exclude_social_media_links=True       # Skip recognized social media domains
        )
        result = await crawler.arun(
            url=url,
            config=crawler_cfg,
        )
        links  = result.links.get("internal", [])
        for x in links:
            text = await get_text(x['href'])
            markdown.append(text)
 


    
    print(markdown)

if __name__ == "__main__":
    asyncio.run(main())