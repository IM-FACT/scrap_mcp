import sys
import os
import requests
import asyncio
import json

from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from brave_search_impl import brave_search_impl
from tool.rewrite_query import rewrite_query
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
    
async def brave_scrap(url: str, keyword: str="default") -> list[str]:
    try:
        result_json = await scrape_web(url, keyword)
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
        kor_queries, eng_queries = rewrite_query(query)
        rewritten_query_list=kor_queries + eng_queries
        print(f"\n[키워드] {rewritten_query_list}")
        results = []
        for r_q in rewritten_query_list:
            partial_results = brave_search_impl(query=r_q, api_key=api_key, count=2)
            results.extend(partial_results)

        valid_results = [res for res in results if is_url_alive(res["url"])]

        if not valid_results:
            print("검색 결과는 있었지만, 유효한 링크가 없음")
            continue

        for idx, item in enumerate(valid_results, 1):
            print(f"\n{idx}. {item['title']}")
            print(f"{item['text']}")
            print(f"{item['url']}")

            full_texts = await brave_scrap(item["url"], rewritten_query_list)

            if not full_texts:
                print("본문 없음 또는 에러 발생")
            elif len(full_texts[0]) < 100:
                print("본문 추출 성공했지만 너무 짧음")
                print(full_texts[0][:100])
            else:
                print("본문 일부:")
                print(full_texts[0][:10000])

# 실행
if __name__ == "__main__":
    asyncio.run(main())
