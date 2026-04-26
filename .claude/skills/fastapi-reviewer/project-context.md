# 이 프로젝트 고유 컨텍스트 (fastapi-reviewer 보조 자료)

SKILL.md에서 필요할 때 이 파일을 Read 하여 로드합니다. 일반 FastAPI 리뷰 원칙 외에 **이 저장소 특유**의 관례만 모았습니다.

## 1. 기술 스택 고정사항

- **Python**: 3.12+ (CLAUDE.md 기준)
- **패키지 매니저**: `uv` — `uv add <pkg>`, `uv run pytest`, `uv run uvicorn ...`. PR에 `pip install`, `requirements.txt` 갱신이 들어오면 **Warning**.
- **서버 기동**: `uv run uvicorn app.main:app --reload --port 8080`
- **기본 JSON 직렬화**: `orjson`. `json.dumps` 호출 추가 → 성능 저하 가능성 **Warning**. `JSONResponse` 대신 `ORJSONResponse` 또는 app 기본 설정 재사용 권장.

## 2. 아키텍처 경계 (app/ 디렉토리)

```
app/
├── main.py                 # FastAPI 엔트리, 미들웨어 등록
├── config.py               # 환경 기반 설정 (ENV, LOG_LEVEL, API_HOST/PORT)
├── routers/                # 엔드포인트 (todos.py 등)
├── models/                 # Pydantic 모델
├── api/                    # JSON 비교 엔드포인트 등 보조 API
└── observability/          # 핵심: 건드리면 추적 깨짐
    ├── logger.py           # 구조화 JSON 로거 (파일 로테이션 hourly, 7일 보존)
    ├── middleware.py       # RequestTrackerMiddleware — UUID 생성 + 흐름
    └── context.py          # request_id 컨텍스트 매니저
```

### 리뷰 시 자주 보는 안티패턴

| 안티패턴 | 심각도 | 이 프로젝트 문맥 |
|---|---|---|
| 라우터에서 `print()` | **Critical** | `app/observability/logger.py` 로거 있음. request_id 흐름 끊김 |
| 새 미들웨어를 `RequestTrackerMiddleware` **앞에** 등록 | **Critical** | request_id가 없는 상태로 로깅 → 추적 불가 |
| `def` 엔드포인트에서 동기 DB/HTTP 호출 | **Critical** | async 환경 블로킹 |
| `response_model` 누락 | Warning | OpenAPI 스펙 품질·검증 저하 |
| `allow_origins=["*"]` 유지 | Warning (prod PR은 Critical) | CLAUDE.md 가 이미 지적 |
| `app/config.py` 우회하여 하드코딩 | Warning | ENV 변수 체계 깨짐 |

## 3. 로깅 규약

- **반드시** `app.observability.logger`의 로거를 쓴다.
- 로그는 `logs/` 에 시간 기반 rotation, 7일 retention.
- 새 로그 필드를 추가할 땐 구조화(key=value JSON) 유지. 자유 텍스트 메시지에 PII 직접 삽입 금지.

## 4. 성능 관련 기준선

성능 이슈로 의심되면 **`/performance-optimizer` 스킬로 위임**. 기준선:

- JSON 직렬화 벤치마크: `tests/test_json_performance.py`, `benchmarks/benchmark_report.py`
- 성능 리포트: `docs/JSON_PERFORMANCE_REPORT.md`
- 성능 엔드포인트: `/json/{library}/{count}`, `/json/compare/{count}`

리뷰에서 "이 변경이 벤치마크에 영향을 줄 수 있다"고 판단되면 **Action Items에 벤치마크 재실행**을 포함.

## 5. 테스트 정책

- `uv run pytest` 로 전체, `uv run pytest tests/test_json_performance.py` 로 개별.
- `pyproject.toml`에 python path 구성됨 → 새 테스트는 `tests/` 하위에 두면 됨.
- 엔드포인트 추가 PR에 테스트 없음 → **Warning** (기존 루즈한 기준에 맞춰, Critical은 아님).

## 6. 학습자 코드와의 구분

`fastapi-mastery/01-fundamentals/` 하위 코드는 **학습 목적**으로, `app/` 프로덕션 코드와 동일한 기준으로 리뷰하면 과도함.

- 해당 경로 파일이면 `/async-mentor` 스킬로 위임 권장.
- 프로덕션 규칙(observability, orjson 강제 등)은 완화해서 적용.

## 7. 의존성 추가 가드

- 동일 기능 라이브러리가 이미 있는가? (e.g., 새 JSON 라이브러리 추가 전 orjson/ujson 비교)
- `uv add` 사용 여부 확인
- 보안 취약점: 최신 메이저 버전인가
