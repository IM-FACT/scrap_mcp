from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from playwright_stealth import stealth_sync
from mcp.server.fastmcp import FastMCP
from bs4 import BeautifulSoup
import lxml
import random
import re
import json
import asyncio

mcp = FastMCP("Scraper")

def keyword_context(texts: list, keyword: str, context_range: int):
    try:
        origin = ' '.join(texts)
        
        key_pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        matche_idxs = [(m.start(), m.end()) for m in key_pattern.finditer(origin)]
        
        if not matche_idxs:
            return []
        
        contexts = []
        for s_idx, e_idx in matche_idxs:
            s_context = max(0, s_idx - context_range)
            e_context = min(len(origin), e_idx + context_range)
            contexts.append((s_context, e_context))
        
        merged_contexts = []
        contexts.sort()
        
        for start, end in contexts:
            if merged_contexts and start <= merged_contexts[-1][1]:
                merged_contexts[-1] = (merged_contexts[-1][0], max(merged_contexts[-1][1], end))
            else:
                merged_contexts.append((start, end))
        
        extracted = []
        results = []
        for start, end in merged_contexts:
            extracted = origin[start:end]
            
            words = extracted.split()
            if len(words) > 1:
                if start > 0:
                    words = words[1:]
                if end < len(origin):
                    words = words[:-1]
            
            if words:
                    results.append(' '.join(words))
            if not results:
                raise ValueError("No results found")
        return results
    
    except Exception as e:
        raise

def center_context(origin: list, max_length: int = 1000):
    full_text = ' '.join(origin)
    if len(full_text) <= max_length:
        return [full_text]

    center = len(full_text) // 2
    half_length = max_length // 2
    
    start = max(0, center - half_length)
    end = min(len(full_text), center + half_length)
    
    if end - start < max_length:
        if start == 0: 
            end = min(len(full_text), start + max_length)
        elif end == len(full_text):
            start = max(0, end - max_length)
    
    extracted = full_text[start:end]
    
    words = extracted.split()
    if len(words) > 1:
        if start > 0: 
            words = words[1:]
        if end < len(full_text):
            words = words[:-1]
    
    result = ' '.join(words).strip()
    if not result:
        raise ValueError("No results found")
    return [result]


async def load_page(url: str):
    texts = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        stealth_sync(page)
        page.route("**/*", lambda route: (
                route.abort() if route.request.resource_type in ["image", "font", "media"]
                else route.continue_()
            ))
        try:
            await page.goto(url)
            page.evaluate("""
                async () => {
                    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
                    const scrollHeight = document.body.scrollHeight;
                    const viewportHeight = window.innerHeight;
                    
                    for (let i = 0; i < scrollHeight; i += viewportHeight) {
                        window.scrollTo(0, i);
                        await delay(100 + Math.random() * 200);
                    }
                }
            """)
            
            for _ in range(3):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                page.mouse.move(x, y)
                page.wait_for_timeout(random.randint(100, 200))

            inside = await page.content()
            soup = BeautifulSoup(inside, 'lxml')
            
            tags = soup.find_all(['div', 'p'])
            
            for tag in tags:
                is_child = False
                for parent in tag.parents:
                    if parent.name in ['div', 'p']:
                        is_child = True
                        break
                
                if not is_child:
                    content = tag.get_text(separator=' ', strip=True)
                    if content:
                        cleaned_text = ' '.join(content.split())
                        texts.append(cleaned_text)

                    
        except PlaywrightTimeoutError:
            browser.close()
            raise
        
        await browser.close()
        
    return texts


@mcp.tool()
async def scrape_web(url: str, keyword: str = "default") -> str:
    """
    Scrape a website of given URL and extract context of given keyword and return all text in JSON style.
    If keyword is not given, all text is returned. limit in 2000 characters.
    URL of contents is in "url" field.
    Keyword is in "keyword" field. If keyword is not given, "default" is used. 
    And it means mid-range text is returned.
    Contexts are in "contexts" field. 
    If error occurs, "fail" field is set.
    """

    result = {}
    result["url"] = url
    result["keyword"] = keyword
    
    try:
        texts = await load_page(url)
        if keyword != "default":
            contexts = keyword_context(texts, keyword, context_range=200)
            result["contexts"] = contexts
        else:
            contexts = center_context(texts, max_length=1500)
            result["contexts"] = contexts

    except ValueError as e:
        result["fail"] = f"Error occurred: {e}"
    except Exception as e:
        result["fail"] = f"Error occurred: {e}"
        
    response = json.dumps(result, ensure_ascii=False)
    return response



if __name__ == '__main__':
    # texts = load_page('https://edition.cnn.com/2025/05/19/middleeast/socotra-trees-yemen-climate-change-intl-hnk')
    # contexts = keyword_context(texts, 'blood', context_range=150)
    
    
    # for i in range(len(contexts)):
    #     print(contexts[i])
    #     print('-'*100)
    asyncio.run(mcp.run())