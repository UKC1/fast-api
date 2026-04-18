# 01-Fundamentals 학습 로드맵

> **목표**: Python 비동기 프로그래밍과 FastAPI 근본 원리를 완전히 체득하기

## 📊 현재 진행 상황

### ✅ 완성된 것들
- **이론 가이드**: `docs/01-async-deep-dive.md` (240줄의 포괄적 비동기 가이드)
- **기초 실습**: `exercises/async-basics/` (코루틴 기초 + 해답)
- **고급 실습**: `exercises/event-loop-control/` (이벤트 루프 제어)
- **실무 예제**: `examples/01_fastapi_async_optimization.py` (프로덕션급 FastAPI)

### 🔄 진행 중인 것들
- 없음 (계획 단계)

### ❌ 아직 안 한 것들
- HTTP 프로토콜 심화 가이드
- 빠진 실습들 (컨텍스트 매니저, 제너레이터, HTTP 요청)
- 미니 프로젝트 3개
- 한국어 학습 가이드
- 참고 자료 정리

## 🗺️ 전체 학습 구조

### Week 1: 비동기 프로그래밍 마스터 (70% 완성)
```
docs/
├── 01-async-deep-dive.md           ✅ 완성
├── 02-http-deep-dive.md             ❌ 없음
└── 03-asgi-ecosystem.md             ❌ 없음

exercises/
├── async-basics/                    ✅ 완성 (기초 + 해답)
├── async-context-manager/           ❌ 빈 폴더
├── async-generator/                 ❌ 빈 폴더
├── concurrent-requests/             ❌ 빈 폴더
└── event-loop-control/              ✅ 완성 (고급 문제만)
```

### Week 2: HTTP & ASGI 심화 (0% 완성)
```
docs/
├── 02-http-deep-dive.md             ❌ HTTP 1.1/2/3 비교, 최적화
├── 03-asgi-ecosystem.md             ❌ WSGI vs ASGI, 서버 비교

exercises/
├── http-mastery/                    ❌ 없음 (HTTP 최적화 실습)
└── asgi-deep-dive/                  ❌ 없음 (ASGI 서버 구현)
```

### Week 3: FastAPI 철학 체득 (30% 완성)
```
docs/
└── 04-fastapi-philosophy.md         ❌ FastAPI 설계 철학, 내부 동작

examples/
├── 01_fastapi_async_optimization.py ✅ 완성 (실무 최적화)
├── 02_custom_middleware.py          ❌ 없음
└── 03_dependency_injection.py       ❌ 없음

projects/
├── custom-asgi-server/              ❌ 빈 폴더
├── async-web-crawler/               ❌ 빈 폴더
└── chat-server/                     ❌ 빈 폴더
```

## 📚 상세 학습 계획

### 1. 이론 문서 (docs/)

#### 01-async-deep-dive.md ✅
- **완성도**: 100%
- **내용**: 이벤트 루프, 코루틴, 고급 패턴, 성능 최적화
- **분량**: 240줄의 상세 가이드

#### 02-http-deep-dive.md ❌
- **목표**: HTTP 프로토콜 최적화 전문가
- **내용 계획**:
  - HTTP/1.1 vs HTTP/2 vs HTTP/3 성능 차이
  - Keep-Alive, 파이프라이닝, 멀티플렉싱
  - 헤더 최적화 및 압축 (GZIP, Brotli)
  - 상태 코드 실무 활용 가이드
  - FastAPI에서 HTTP 기능 최대 활용법

#### 03-asgi-ecosystem.md ❌
- **목표**: ASGI 생태계 완전 이해
- **내용 계획**:
  - WSGI vs ASGI 아키텍처 비교
  - Uvicorn, Gunicorn, Hypercorn 벤치마킹
  - 미들웨어 스택 실행 순서와 최적화
  - 연결 풀링과 리소스 관리

#### 04-fastapi-philosophy.md ❌
- **목표**: FastAPI 설계 철학 체득
- **내용 계획**:
  - Sebastian Ramirez의 설계 철학 분석
  - Python 타입 힌트 시스템 완전 활용
  - Pydantic 내부 동작과 성능 최적화
  - OpenAPI/JSON Schema 자동 생성 메커니즘

### 2. 실습 연습 (exercises/)

#### async-basics/ ✅
- **완성도**: 100%
- **파일**: 기초 문제 + 완전한 해답
- **난이도**: 초급 → 중급

#### async-context-manager/ ❌
- **목표**: 비동기 컨텍스트 매니저 마스터
- **실습 계획**:
  - 데이터베이스 연결 관리
  - 파일 I/O 최적화
  - 리소스 자동 정리
  - 에러 핸들링과 롤백

#### async-generator/ ❌
- **목표**: 비동기 제너레이터 활용
- **실습 계획**:
  - 대용량 데이터 스트리밍
  - 무한 시퀀스 처리
  - 메모리 효율적 데이터 처리
  - FastAPI 스트리밍 응답

#### concurrent-requests/ ❌
- **목표**: HTTP 요청 동시 처리 마스터
- **실습 계획**:
  - 여러 API 동시 호출
  - 타임아웃과 재시도 로직
  - 서킷 브레이커 구현
  - 요청 배칭과 스로틀링

#### event-loop-control/ 🔄
- **완성도**: 70% (고급 문제만 있음)
- **추가 필요**: 기초부터 단계적 학습 과정

### 3. 실무 예제 (examples/)

#### 01_fastapi_async_optimization.py ✅
- **완성도**: 100%
- **내용**: 프로덕션급 FastAPI 최적화 패턴

#### 추가 예제 계획 ❌
- **02_custom_middleware.py**: 미들웨어 개발 패턴
- **03_dependency_injection.py**: 의존성 주입 고급 활용
- **04_websocket_chat.py**: WebSocket 실시간 통신
- **05_streaming_responses.py**: 스트리밍 응답 최적화

### 4. 미니 프로젝트 (projects/)

#### custom-asgi-server/ ❌
- **목표**: ASGI 서버 직접 구현으로 내부 동작 이해
- **기능**: 기본 HTTP 처리, 미들웨어 지원, 웹소켓
- **예상 시간**: 4-6시간

#### async-web-crawler/ ❌
- **목표**: 대규모 웹 크롤링으로 동시성 마스터
- **기능**: 동시 요청 제어, 로봇 규칙 준수, 데이터 저장
- **예상 시간**: 3-4시간

#### chat-server/ ❌
- **목표**: WebSocket으로 실시간 통신 구현
- **기능**: 다중 채팅방, 사용자 관리, 메시지 브로드캐스트
- **예상 시간**: 2-3시간

### 5. 학습 자료 (resources/)

#### 계획된 내용 ❌
- **async_cheatsheet.md**: 비동기 프로그래밍 치트시트
- **fastapi_patterns.md**: FastAPI 패턴 모음
- **performance_tips.md**: 성능 최적화 팁
- **common_pitfalls.md**: 흔한 실수와 해결법
- **useful_links.md**: 유용한 참고 링크 모음

## 🎯 학습 순서 권장사항

### 초보자 (비동기 프로그래밍 처음)
1. `docs/01-async-deep-dive.md` 정독
2. `exercises/async-basics/` 완전 정복
3. `exercises/async-context-manager/` 실습
4. `examples/01_fastapi_async_optimization.py` 분석

### 중급자 (비동기 기초 있음)
1. `exercises/event-loop-control/` 도전
2. `docs/02-http-deep-dive.md` 학습
3. `projects/custom-asgi-server/` 구현
4. `projects/async-web-crawler/` 구현

### 고급자 (FastAPI 경험 있음)
1. `docs/04-fastapi-philosophy.md` 심화 학습
2. `projects/chat-server/` 구현
3. 모든 예제 최적화 도전
4. 새로운 패턴 실험

## 📈 학습 성과 측정

### 기술 역량 체크리스트
- [ ] 1000+ 동시 연결 처리하는 서버 구현
- [ ] 메모리 사용량 50% 이하로 최적화
- [ ] HTTP/2 서버 직접 구현
- [ ] FastAPI 핵심 기능 재구현
- [ ] N+1 쿼리 문제 완전 해결

### 실무 적용 체크리스트
- [ ] 프로덕션 환경에서 안정적 운영
- [ ] 복잡한 비동기 문제 디버깅 가능
- [ ] 팀원들에게 비동기 개념 설명 가능
- [ ] 성능 병목 지점 즉시 식별
- [ ] 새로운 비동기 패턴 창조적 적용

## 📝 학습 일지

### 2024-04-18 (금)
- ✅ 전체 프레임워크 구축 완료
- ✅ 01-async-deep-dive.md 작성 (240줄)
- ✅ async-basics 실습 완성 (기초 + 해답)
- ✅ event-loop-control 고급 실습 작성
- ✅ FastAPI 최적화 예제 완성
- 🎯 **다음 목표**: 빠진 실습들 완성

---

**💡 학습 팁**: 이론보다 실습에 더 많은 시간을 할애하세요. 코드를 직접 작성하고 실행해보는 것이 가장 효과적입니다.