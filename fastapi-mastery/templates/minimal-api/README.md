# 🔰 Minimal FastAPI Template

> **목표**: 단일 파일로 빠른 프로토타이핑과 API 개발 시작하기

## ⚡ 빠른 시작

### 1. 의존성 설치
```bash
# UV 사용 (권장)
uv add fastapi uvicorn

# 또는 pip 사용
pip install -r requirements.txt
```

### 2. 서버 실행
```bash
# 직접 실행
python main.py

# 또는 uvicorn 사용
uvicorn main:app --reload
```

### 3. API 사용해보기
- **Swagger UI**: http://localhost:8000/
- **API 엔드포인트**: http://localhost:8000/items

## 🎯 제공 기능

### 📋 기본 CRUD 작업
```http
GET    /items           # 모든 아이템 조회
POST   /items           # 새 아이템 생성
GET    /items/{id}      # 특정 아이템 조회
PUT    /items/{id}      # 아이템 수정
DELETE /items/{id}      # 아이템 삭제
```

### 🔍 고급 기능
```http
GET    /health          # 서버 상태 확인
GET    /items?search=keyword&skip=0&limit=10  # 검색 및 페이지네이션
GET    /stats           # 통계 정보
```

## 🧪 API 테스트 예시

### 1. 새 아이템 생성
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "FastAPI 학습",
    "description": "프레임워크 마스터하기",
    "tags": ["python", "api"]
  }'
```

### 2. 아이템 목록 조회
```bash
curl "http://localhost:8000/items"
```

### 3. 검색
```bash
curl "http://localhost:8000/items?search=FastAPI&limit=5"
```

### 4. 통계 확인
```bash
curl "http://localhost:8000/stats"
```

## 🔧 커스터마이징

### 데이터 모델 확장
```python
class Item(ItemBase):
    id: int
    priority: int = Field(default=1, ge=1, le=5)  # 우선순위 추가
    due_date: Optional[datetime] = None           # 마감일 추가
    status: str = Field(default="pending")        # 상태 추가
```

### 새 엔드포인트 추가
```python
@app.get("/items/urgent", tags=["Items"])
async def get_urgent_items():
    """긴급한 아이템만 조회"""
    urgent_items = [
        item for item in items_storage.values() 
        if item.priority >= 4
    ]
    return urgent_items
```

### 인증 추가 (선택사항)
```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.get("/protected")
async def protected_route(token: str = Depends(security)):
    # 토큰 검증 로직
    return {"message": "인증된 사용자만 접근 가능"}
```

## 📈 다음 단계

### 기능 확장
1. **데이터베이스 연동**: SQLite → PostgreSQL
2. **인증 시스템**: JWT 토큰 기반 인증
3. **파일 업로드**: 이미지 및 문서 업로드
4. **실시간 업데이트**: WebSocket 연동

### 구조 개선
1. **모듈 분리**: 라우터, 모델, 서비스 분리
2. **설정 관리**: 환경변수 기반 설정
3. **로깅 시스템**: 구조화된 로깅
4. **테스트 추가**: 단위 테스트 및 통합 테스트

### 프로덕션 준비
```bash
# 다른 템플릿으로 마이그레이션
cp -r templates/structured-api my-project
cd my-project
```

## 💡 활용 사례

### 1. API 프로토타이핑
- 아이디어 검증을 위한 빠른 MVP 개발
- 클라이언트 개발자와의 API 스펙 논의

### 2. 학습 및 실험
- FastAPI 기능 테스트
- 새로운 라이브러리 통합 실험

### 3. 마이크로서비스
- 단순한 마이크로서비스 구현
- 서비스 간 통신 테스트

---

**🚀 이제 main.py를 실행하고 API 개발을 시작해보세요!**