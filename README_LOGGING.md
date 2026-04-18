# JSON Performance & Logging System

## 개요
FastAPI 애플리케이션에 JSON 라이브러리 성능 비교 시스템과 request_id 기반의 observability 로깅 시스템을 구축했습니다.

## 주요 기능

### 1. JSON 라이브러리 성능 비교
- **지원 라이브러리**: standard json, orjson, ujson
- **API 엔드포인트**:
  - `/json/standard/{count}` - 표준 JSON 라이브러리 테스트
  - `/json/orjson/{count}` - orjson 라이브러리 테스트  
  - `/json/ujson/{count}` - ujson 라이브러리 테스트
  - `/json/compare/{count}` - 모든 라이브러리 비교

### 2. Observability 시스템
- **Request ID 추적**: 모든 요청에 고유 ID 부여
- **구조화된 JSON 로깅**: 분석이 쉬운 JSON 형식
- **시간별 로그 로테이션**: 매시간 새 파일 생성, 7일간 보관
- **성능 메트릭 로깅**: API 응답 시간 자동 기록

## 로그 파일 구조
```
logs/
├── app.log              # 애플리케이션 전반 로그
├── json_comparison.log  # JSON 성능 비교 로그
├── middleware.log       # 미들웨어 로그
└── performance.log      # 성능 전용 로그
```

## 성능 테스트 실행
```bash
# 서버 시작
uv run uvicorn app.main:app --reload --port 8080

# 성능 테스트 실행
uv run python tests/test_json_performance.py
```

## 로그 확인 방법
```bash
# 실시간 로그 모니터링
tail -f logs/json_comparison.log

# JSON 포맷으로 보기
cat logs/performance.log | python -m json.tool
```

## 테스트 결과 예시
- **orjson**: 가장 빠른 인코딩/디코딩 속도 (표준 대비 2-7배 빠름)
- **ujson**: orjson 다음으로 빠른 성능
- **standard json**: 기본 라이브러리, 호환성 최고

## 환경 설정 (app/config.py)
- `LOG_LEVEL`: 로그 레벨 설정 (기본: INFO)
- `LOG_TO_FILE`: 파일 로깅 활성화 (기본: local 환경에서만)
- `LOG_ROTATION`: 로그 로테이션 주기 (기본: H - 시간별)
- `LOG_BACKUP_COUNT`: 보관 파일 수 (기본: 168개 - 7일)