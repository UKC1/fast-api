# JSON 직렬화 성능 최적화 프로젝트

## 프로젝트 구조

```
fast-api/
├── app/
│   ├── api/
│   │   └── json_comparison.py      # JSON 라이브러리 비교 API
│   ├── observability/              # 로깅 및 모니터링
│   │   ├── __init__.py
│   │   ├── context.py             # Request ID 추적
│   │   ├── logger.py              # 구조화된 JSON 로깅
│   │   └── middleware.py          # 요청 추적 미들웨어
│   └── main.py                    # FastAPI 앱 진입점
│
├── benchmarks/                     # 성능 벤치마크
│   ├── benchmark_report.py       # 벤치마크 실행 스크립트
│   └── benchmark_results.json    # 벤치마크 결과 데이터
│
├── docs/                          # 문서
│   └── JSON_PERFORMANCE_REPORT.md # 상세 성능 분석 보고서
│
├── examples/                      # 예제 코드
│   ├── serialization_demo.py    # 직렬화 성능 데모
│   ├── fastapi_optimization.py  # FastAPI 최적화 패턴
│   └── performance_comparison.py # Pydantic vs JSON 비교
│
├── logs/                         # 로그 파일 (시간별 로테이션)
│   ├── app_2024-01-22_15.log   # 애플리케이션 로그
│   ├── performance.log         # 성능 메트릭 로그
│   └── json_comparison.log     # JSON 비교 전용 로그
│
└── tests/                       # 테스트 코드
    └── test_json_performance.py # 성능 테스트
```

## 빠른 시작

### 1. 의존성 설치 (UV 사용)

```bash
# UV로 의존성 설치
uv add orjson ujson msgpack

# 개발 서버 실행
uv run uvicorn app.main:app --reload --port 8080
```

### 2. 성능 테스트 실행

```bash
# 직렬화 데모 실행
uv run python examples/serialization_demo.py

# 벤치마크 실행
uv run python benchmarks/benchmark_report.py
```

### 3. API 테스트

```bash
# 표준 JSON
curl http://localhost:8080/json/standard/1000

# orjson (가장 빠름)
curl http://localhost:8080/json/orjson/1000

# 전체 비교
curl http://localhost:8080/json/compare/1000
```

## 핵심 개념

### 직렬화가 왜 중요한가?

```
클라이언트 요청
    ↓
FastAPI 라우터
    ↓
비즈니스 로직
    ↓
Pydantic 검증 (30% 시간)  ← 데이터 안정성
    ↓
JSON 직렬화 (70% 시간)    ← orjson으로 최적화!
    ↓
HTTP 응답
```

### 성능 비교 (10,000 레코드)

| 라이브러리 | 속도 향상 | 용도 |
|-----------|---------|------|
| json | 1x (기준) | 호환성 중요 |
| ujson | 1.1x | 범용 |
| orjson | **4.8x** | 고성능 API |
| msgpack | 3.4x | 바이너리 통신 |

## 실무 적용 예시

### 1. FastAPI 기본 설정

```python
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    default_response_class=ORJSONResponse  # 전역 적용
)
```

### 2. 조건부 최적화

```python
@app.get("/users")
async def get_users(validate: bool = True):
    if validate:
        # Pydantic 검증 필요할 때
        return [User(**data) for data in raw_data]
    else:
        # 빠른 응답 필요할 때
        return ORJSONResponse(raw_data)
```

### 3. 캐싱 전략

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_json(query: str) -> bytes:
    data = fetch_data(query)
    return orjson.dumps(data)  # 직렬화된 상태로 캐싱
```

## 모니터링

### 로그 확인

```bash
# 실시간 로그 모니터링
tail -f logs/app_*.log

# JSON 성능 로그
tail -f logs/json_comparison.log | jq '.'
```

### 성능 메트릭

로그에 포함되는 메트릭:
- `encode_ms`: 인코딩 시간
- `decode_ms`: 디코딩 시간
- `data_size`: 데이터 크기
- `request_id`: 요청 추적 ID

## 다음 단계

1. **프로파일링**: `py-spy`로 병목 지점 찾기
2. **비동기 최적화**: `asyncio` 활용도 개선
3. **데이터베이스 최적화**: ORM vs Raw SQL
4. **캐싱 확장**: Redis 통합
5. **압축**: Brotli/Gzip 응답 압축

## 참고 자료

- [docs/JSON_PERFORMANCE_REPORT.md](docs/JSON_PERFORMANCE_REPORT.md) - 상세 분석
- [examples/](examples/) - 실행 가능한 예제 코드
- [benchmarks/](benchmarks/) - 성능 측정 도구

---

*이 프로젝트는 Python 백엔드 성능 최적화 연구의 일환입니다.*