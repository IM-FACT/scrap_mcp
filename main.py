from mcp.server.fastmcp import FastMCP
import json
import asyncio
import sys
import io
import re

from tool.text import use_tra
from tool.bing import use_bing
from tool.goo_api import use_google

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
mcp = FastMCP("Scraper")

@mcp.tool()
async def scrape_web(url: str) -> str:
    """
    Scrape a website of given URL and extract context of given keyword and return all text in JSON style.
    URL of contents is in "url" field.
    Keyword is in "keyword" field. If keyword is not given, "default" is used. 
    If keyword is not given, mid-range text is returned..
    Bing and Google search results on URL are in "bing" and "google" field.
    General HTTP Request result is in "normal" field.
    """

    result = {}
    result["url"] = url
    result["keyword"] = keyword
    
    result["bing"] = await use_bing(url)
    result["google"] = await use_google(url)
    result["normal"] = use_tra(url, keyword=keyword)
    
    response = json.dumps(result, ensure_ascii=False)
    cleaned = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', response)
    
    print(cleaned)
    return cleaned



if __name__ == '__main__':
    #asyncio.run(scrape_web("https://www.bbc.com/news/articles/cd0n1m4r99zo"))
    asyncio.run(mcp.run())
    # texts = load_page('https://edition.cnn.com/2025/05/19/middleeast/socotra-trees-yemen-climate-change-intl-hnk')
    # contexts = keyword_context(texts, 'blood', context_range=150)
    
    
    # for i in range(len(contexts)):
    #     print(contexts[i])
    #     print('-'*100)