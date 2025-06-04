from brave_search_impl import brave_search_impl
import sys
import os
import requests
import asyncio
import json
from dotenv import load_dotenv
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from main import scrape_web


load_dotenv()
api_key = os.getenv("BRAVE_AI_API_KEY")

# 유효한 URL인지 확인
def is_url_alive(url: str) -> bool:
    try:
        if "jsessionid" in url.lower():
            return False
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=5)
        if res.status_code != 200:
            return False
        error_keywords = ["존재하지 않는", "not found", "세션이 만료"]
        return not any(keyword in res.text.lower() for keyword in error_keywords)
    except requests.RequestException:
        return False

# MCP POST 방식 대신, 직접 함수 호출
# async def extract_text_from_url_local(url: str, keyword: str = "default") -> list[str]:
#     try:
#         result_json = await scrape_web(url, keyword)
#         result = json.loads(result_json)
#         return result.get("contexts", [])
#     except Exception as e:
#         print(f"스크래퍼 호출 실패: {e}")
#         return []
# 만약 scrape_web이 content 필드에 str로 줄 경우
async def extract_text_from_url_local(url: str) -> list[str]:
    try:
        result_json = await scrape_web(url)
        result = json.loads(result_json)
        content = result.get("content", "")
        if isinstance(content, str):
            return [content]
        else:
            return []
    except Exception as e:
        print(f"스크래퍼 호출 실패: {e}")
        return []



# 테스트용 메인 함수
async def main():
    test_queries = ["이상 기후 현상?"]

    for query in test_queries:
        print(f"\n[질문] {query}")
        results = brave_search_impl(query=query, api_key=api_key, count=5)

        valid_results = [res for res in results if is_url_alive(res["url"])]

        if not valid_results:
            print("검색 결과는 있었지만, 유효한 링크가 없음")
            continue

        for idx, item in enumerate(valid_results, 1):
            print(f"\n{idx}. {item['title']}")
            print(f"{item['text']}")
            print(f"{item['url']}")

            # full_texts = await extract_text_from_url_local(item["url"], keyword="기후")
            full_texts = await extract_text_from_url_local(item["url"])

            if not full_texts:
                print("본문 없음 또는 에러 발생")
            elif len(full_texts[0]) < 100:
                print("본문 추출 성공했지만 너무 짧음")
            else:
                print("본문 일부:")
                print(full_texts[0][:10000])

# 실행
if __name__ == "__main__":
    asyncio.run(main())
