from mcp.server.fastmcp import FastMCP
import httpx
import json
import lxml
from bs4 import BeautifulSoup

mcp = FastMCP("Scraper")

@mcp.tool()
async def scrape_web(url: str) -> str:
    """
    Scrape a website of given URL and return all text in JSON style.
    Contents are in "content" field.
    If error occurs, "fail" field is set.
    URL of contents is in "url" field.
    """
    
    result = {}
    result["url"] = url

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
        
        docs = BeautifulSoup(response.text, "lxml")
            
        result["content"] = docs.get_text()

    except httpx.HTTPError as e:
        result["fail"] = f"HTTP error occurred: {e}"
    except Exception as e:
        result["fail"] = f"Error occurred: {e}"
        
    response = json.dumps(result, ensure_ascii=False)
    return response


if __name__ == "__main__":
    main()
