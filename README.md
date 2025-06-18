# Web Scraper MCP Server

## 개요
웹 페이지로부터 신뢰도 높은 정보를 수집하고 정제된 텍스트를 반환하는 스크래핑 시스템입니다.
GPT 4o 키워드 리라이팅 + Brave Search API → URL 수집 → 본문 스크래핑 → 본문 추출 → GPT 4-turbo로 답변 생성 과정을 수행하며,
OpenAI API 기반 질문 답변용 RAG 시스템의 외부 문서 수집 컴포넌트로 사용됩니다.

## 설치 및 설정
### 환경 변수 설정 (.env 파일)
```bash
GOOGLE_API_KEY=your_google_key        # Google Custom Search API
OPENAI_API_KEY=your_openai_key        # OpenAI API
BRAVE_AI_API_KEY=your_brave_key       # Brave Search API for Data for AI
```

> Google API 설정 필요(무료 : 하루 100회 요청)
https://developers.google.com/custom-search/v1/overview?hl=ko#api_key

> Brave Search API는 Brave 계정에서 발급 가능 
https://search.brave.com/api

### Python 패키지 설치
```bash
uv sync
playwright install  # 웹드라이버 의존성 설치
```

## 사용법

playwright가 실제 웹을 통해 작동하므로 유의바람

### 키워드 기반 스크래핑 실행
```bash
mcp dev main.py
```
### 키워드 리라이팅 + Brave Search + 스크래핑 + 답변 생성 테스트
```bash
python scrap_mcp/tests/test_mcp_module.py
```


### 스크래핑 응답 형식
```json
{
  "url": "https://example.com",
  "keyword": "검색 키워드",
  "page": {
    "title": "페이지 제목",
    "description": "메타 디스크립션",
    "content": "본문 전체 내용"
  },
  "google": "구글 스니펫 (본문 없을 경우)",
  "normal": "정상 HTTP 응답 본문"
}

```
normal → google → page.description 순으로 우선순위가 적용되어 최종 문서가 추출됩니다.

## 디렉토리 구조
```bash
scrap_mcp/
├── main.py               # Scraper 모듈
├── mcp_module.py         # GPT 4o 키워드 리라이팅 + Brave Search + Scraper + GPT 4-turbo 답변 생성 연동
├── brave_search_module/
│   └── brave_search_impl.py  # Brave Search API Data for AI 모듈
│   └── brave_search_test.py  # Brave Search API 테스트
├── prompts/
│   ├── generate_ans_prompt.txt      # GPT 4-turbo 답변 생성용 프롬프트
│   └── rewrite_query_prompt.txt     # GPT 4o 키워드 리라이팅용 프롬프트
├── tool/
│   ├── gen_ans.py           # GPT 4-turbo 기반 답변 생성 모듈
│   ├── rewrite_query.py     # Keyword rewriting 모듈
│   ├── bing.py
│   ├── goo_api.py
│   └── text.py
├── tests/
│   └── test_mcp_module.py  # 테스트 코드
```
## 오류 처리

- 응답 JSON에 실패시 해당하는 메시지가 출력
- 페이지가 없거나 403/404 응답 시 Google/Bing 스니펫으로 대체

## 스크래핑 설정

- `headless=False`: 가능한 한 봇 체크를 피하기 위함
- `context_range=200`: 키워드 주변 추출 범위
- `max_length=1500`: 중앙 부분 추출 시 범위 
