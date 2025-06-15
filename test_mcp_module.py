# test_mcp_module.py
import asyncio
from mcp_module import search_scrap

query = "미세먼지가 심한 날 비가 오면 '씻겨 내려간다'고 하는데, 실제로 비가 미세먼지를 줄여주는 효과가 있나? 미세먼지와 날씨의 관계가 궁금함"

docs = asyncio.run(search_scrap(query))

for i, doc in enumerate(docs, 1):
    print(f"\n- {i}번 문서")
    print(doc[:5000])