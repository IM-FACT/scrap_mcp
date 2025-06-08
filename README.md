# Web Scraper MCP Server

## 개요
웹페이지에서 텍스트를 스크래핑하고 특정 키워드 주변의 컨텍스트를 추출하는 MCP(Model Context Protocol) 서버입니다. 
기본적으로 trafilatura을 통해 웹을 요청 후 추출하고, 불가능한 사이트에 대응하기 위해 Google API와 Playwright를 이용한 bing 검색을 수행하여 스니펫을 가져옵니다.

## 설치 및 설정

Google API 설정 필요(무료 : 하루 100회 요청)
https://developers.google.com/custom-search/v1/overview?hl=ko#api_key
>> .env 파일에 GOOGLE_API_KEY = '__KEY__'

```bash
uv sync
playwright install  # 웹드라이버 의존성 설치
```

## 사용법

playwright가 실제 웹을 통해 작동하므로 유의바람

### 테스트
```bash
mcp dev main.py
```


### 응답 형식
```json
{
  "url": "https://example.com",
  "keyword": "검색키워드",
  "bing": "빙 검색내용"
  "google" : "구글 검색내용"
  "normal" : "일반 HTTP 요청 내용"
}
```
## 오류 처리

- 응답 JSON에 실패시 해당하는 메시지가 출력

## 스크래핑 설정

- `headless=False`: 가능한 한 봇 체크를 피하기 위함
- `context_range=200`: 키워드 주변 추출 범위
- `max_length=1500`: 중앙 부분 추출 시 범위 
