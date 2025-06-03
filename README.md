# Web Scraper MCP Server

## 개요
웹페이지에서 텍스트를 스크래핑하고 특정 키워드 주변의 컨텍스트를 추출하는 MCP(Model Context Protocol) 서버입니다. Playwright와 BeautifulSoup을 사용하여 동적 웹사이트를 처리합니다.

## 설치 및 설정

```bash
uv sync
playwright install  # 웹드라이버 의존성 설치
```

## 사용법

실제 브라우저를 사용해서 작동하므로 요청 시 브라우저가 켜졌다가 꺼질 것입니다.

### 테스트
```bash
mcp dev main.py
```


### 응답 형식
```json
{
  "url": "https://example.com",
  "keyword": "검색키워드",
  "contexts": [
    "키워드 주변의 컨텍스트 텍스트...",
    "또 다른 컨텍스트..."
  ]
}
```

## 핵심 함수

### `load_page(url: str)`
- 웹페이지 로딩 및 텍스트 추출
- Playwright를 사용한 동적 콘텐츠 처리

### `keyword_context(texts: list, keyword: str, context_range: int)`
- 키워드 주변 컨텍스트 추출
- 겹치는 영역 자동 병합
- 정규식을 사용 검색

### `center_context(origin: list, max_length: int)`
- 키워드가 없을 때 중앙 부분 텍스트 추출
- 맨 앞과 뒤는 메뉴같은 불필요한 정보일 것이라 가정

## 오류 처리

- **내부 작동 문제**: 오류 메시지가 반환되나
- **스크래핑 불가능한 페이지**: CAPTCHA가 존재하거나 비정상적인 접근임을 감지하는 경우 `"MCP error -32001: Request timed out"` 에러가 반환됨

## 스크래핑 설정

- `headless=False`: 가능한 한 봇 체크를 피하기 위함
- `context_range=200`: 키워드 주변 추출 범위
- `max_length=1500`: 중앙 부분 추출 시 범위 