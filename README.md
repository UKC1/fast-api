네, 인코딩이 깨진 Markdown 파일의 내용을 복원했습니다.

FastAPI로 'Todo 리스트'를 만드는 튜토리얼 문서 같네요. 아래 복원된 내용을 확인해 보세요\!

-----

# FastAPI 튜토리얼 - Basic Todo List 만들기

## 🏁 학습 목표

  - FastAPI로 기본 프로젝트 구성하기
  - RESTful API 개념 이해
  - Pydantic을 사용한 데이터 유효성 검사
  - CRUD(Create, Read, Update, Delete) 기능 구현
  - API 문서 자동화 이해

## 📁 프로젝트 구조

```
fast-api/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI 앱 설정
│   ├── models.py       # 데이터 모델 정의
│   └── routes.py       # API 라우터
├── pyproject.toml      # 프로젝트 의존성
└── README.md          # (현재 파일)
```

## 🛠️ 개발 단계

### 1단계: 환경 설정 및 기본 앱 생성

**목표**: FastAPI 앱의 기본 프로젝트 구조와 환경 설정을 완료합니다.

#### ✏️ 세부 작업

1.  `app/main.py`에 FastAPI 인스턴스 생성
2.  루트 라우트(`/`) 엔드포인트 작성
3.  앱 타이틀, 설명 등 설정

#### ✅ 체크리스트

  - [ ] `from fastapi import FastAPI`로 FastAPI 임포트
  - [ ] `app = FastAPI()` 인스턴스 생성
  - [ ] 앱 제목, 설명, 버전 설정
  - [ ] 루트 엔드포인트가 "Welcome" 메시지 반환
  - [ ] `uvicorn`으로 로컬 서버 실행 테스트

### 2단계: 데이터 모델 정의

**목표**: Pydantic을 사용하여 Todo 아이템의 데이터 모델을 정의합니다.

#### ✏️ 세부 작업

1.  `app/models.py`에 Todo 모델 정의
2.  데이터 타입 및 유효성 검사 규칙 설정
3.  생성(Create) 및 수정(Update)을 위한 별도 모델 정의

#### ✅ 체크리스트

  - [ ] `from pydantic import BaseModel` 임포트
  - [ ] Todo 기본 모델 정의 (id, title, description, completed)
  - [ ] 데이터 타입 명시 (str, bool, int)
  - [ ] 기본값 설정 (completed = False)
  - [ ] `Field()`를 사용한 유효성 검사 추가 (예: title의 최소/최대 길이)

### 3단계: 인메모리 데이터베이스 설정

**목표**: 실제 데이터베이스 대신 간단한 리스트(List)로 Todo 데이터를 관리합니다.

#### ✏️ 세부 작업

1.  전역 리스트로 Todo 목록 저장
2.  ID 자동 증가를 위한 카운터 구현
3.  Todo를 찾는 헬퍼 함수 생성

#### ✅ 체크리스트

  - [ ] 전역 변수 `todos = []` 생성
  - [ ] `next_id` 변수로 ID 관리
  - [ ] ID로 특정 Todo를 찾는 함수 구현

### 4단계: CRUD API 라우터 구현

**목표**: RESTful API 원칙에 따라 Todo 항목의 CRUD API를 구현합니다.

#### ✏️ 세부 작업

1.  `app/routes.py`에 API 라우터(Router) 구현
2.  각 기능별 HTTP 메서드 사용
3.  예외 처리 및 상태 코드(Status Code) 설정

#### ✅ 체크리스트

**GET /todos** - 모든 Todo 조회

  - [ ] 전체 todos 리스트 반환
  - [ ] 응답 상태 200

**POST /todos** - 새 Todo 생성

  - [ ] 요청 본문에서 Todo 데이터 받기
  - [ ] ID 할당 및 `next_id` 증가
  - [ ] 생성된 todo 반환
  - [ ] 응답 상태 201 (Created)

**GET /todos/{todo\_id}** - 특정 Todo 조회

  - [ ] 경로 파라미터로 ID 받기
  - [ ] 해당 ID의 todo 반환
  - [ ] 없으면 404 (Not Found) 처리

**PUT /todos/{todo\_id}** - Todo 수정

  - [ ] 경로 파라미터와 요청 본문 받기
  - [ ] 해당 todo 업데이트
  - [ ] 수정된 todo 반환
  - [ ] 없으면 404 (Not Found) 처리

**DELETE /todos/{todo\_id}** - Todo 삭제

  - [ ] 경로 파라미터로 ID 받기
  - [ ] 해당 todo 삭제
  - [ ] 성공 메시지 반환
  - [ ] 없으면 404 (Not Found) 처리

### 5단계: 라우터 통합 및 문서화

**목표**: `main.py`에서 라우터를 통합하고 자동 생성된 문서를 확인합니다.

#### ✏️ 세부 작업

1.  `app/main.py`에 라우터 포함
2.  API 태그 및 접두사(prefix) 설정
3.  자동 생성된 문서 확인

#### ✅ 체크리스트

  - [ ] `APIRouter` 임포트 및 라우터 생성
  - [ ] `app.include_router()`로 라우터 포함
  - [ ] prefix="/todos", tags=["todos"] 설정
  - [ ] `http://localhost:8000/docs`에서 문서 확인

## 🚀 로컬 실행 및 테스트

### 로컬 실행

1.  서버 실행: `uvicorn app.main:app --reload`
2.  브라우저에서 `http://localhost:8000` 접속
3.  API 문서 `http://localhost:8000/docs` 확인

### API 테스트 예시 (curl)

```bash
# 1. Todo 생성
curl -X POST "http://localhost:8000/todos" \
     -H "Content-Type: application/json" \
     -d '{"title": "FastAPI 공부", "description": "기본 튜토리얼 완료"}'

# 2. 모든 Todo 조회
curl -X GET "http://localhost:8000/todos"

# 3. 특정 Todo 조회
curl -X GET "http://localhost:8000/todos/1"

# 4. Todo 수정
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "FastAPI 튜토리얼", "description": "기본 기능 완료", "completed": true}'

# 5. Todo 삭제
curl -X DELETE "http://localhost:8000/todos/1"
```

## 🌟 주요 개념 요약

### FastAPI 핵심 기능

1.  **자동 문서화**: `/docs` (Swagger UI), `/redoc` (ReDoc)
2.  **데이터 유효성 검사**: Pydantic 모델 기반
3.  **비동기 지원**: `async`/`await` 기본 지원
4.  **의존성 주입**: 강력한 DI(Dependency Injection) 시스템

### (참고) HTTP 상태 코드

  - **200 OK**: 요청 성공 (GET, PUT)
  - **201 CREATED**: 리소스 생성 성공 (POST)
  - **204 No Content**: 응답 본문 없음 (DELETE)
  - **404 Not Found**: 리소스를 찾을 수 없음
  - **422 Unprocessable Entity**: 요청 데이터 유효성 검사 실패

## 📚 다음 단계 ( 심화)

1.  **에러 핸들링**: 공통 에러 응답을 위한 예외 처리기 추가
2.  **데이터베이스**: 인메모리 대신 실제 DB 연결 (예: SQLite, PostgreSQL)
3.  **인증**: OAuth2/JWT 등을 사용한 사용자 인증/인가
4.  **테스트**: `pytest`를 사용한 단위 테스트, 통합 테스트 작성
5.  **배포**: Docker, AWS/GCP 등을 사용한 배포

-----

## 🎁 정답 코드 예시 (클릭해서 펼쳐보세요\!)

\<details\>
\<summary\>💡 app/main.py 코드 예시\</summary\>

```python
from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Basic Todo List API",
    description="FastAPI 튜토리얼을 위한 기본 TODO 리스트 API입니다.",
    version="1.0.0"
)

# /todos 접두사와 "todos" 태그로 라우터 포함
app.include_router(router, prefix="/todos", tags=["todos"])

@app.get("/")
async def root():
    return {"message": "Welcome to Basic Todo List API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

\</details\>

\<details\>
\<summary\>💡 app/models.py 코드 예시\</summary\>

```python
from pydantic import BaseModel, Field
from typing import Optional

class TodoBase(BaseModel):
    # Field를 사용하여 유효성 검사 및 문서화 추가
    title: str = Field(..., min_length=1, max_length=100, description="할 일 제목")
    description: Optional[str] = Field(None, max_length=500, description="할 일 상세 설명")
    completed: bool = Field(False, description="완료 여부")

class TodoCreate(TodoBase):
    # 생성 시에는 title만 필수
    pass

class TodoUpdate(BaseModel):
    # 수정 시에는 모든 필드가 선택적(Optional)
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool] = None

class Todo(TodoBase):
    # DB나 응답에서 사용될 전체 모델 (ID 포함)
    id: int = Field(..., description="할 일 ID")
    
    class Config:
        # ORM 모드 (이 예제에서는 크게 중요하지 않음)
        from_attributes = True
```

\</details\>

\<details\>
\<summary\>💡 app/routes.py 코드 예시\</summary\>

```python
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import Todo, TodoCreate, TodoUpdate

router = APIRouter()

# 인메모리 데이터베이스 (간단한 리스트)
todos: List[Todo] = []
next_id = 1

def find_todo(todo_id: int) -> Todo:
    """ID로 Todo를 찾는 헬퍼 함수"""
    for todo in todos:
        if todo.id == todo_id:
            return todo
    return None

@router.get("/", response_model=List[Todo])
async def get_todos():
    """모든 Todo 목록을 조회합니다."""
    return todos

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_create: TodoCreate):
    """새로운 Todo를 생성합니다."""
    global next_id
    new_todo = Todo(
        id=next_id,
        title=todo_create.title,
        description=todo_create.description,
        completed=todo_create.completed
    )
    todos.append(new_todo)
    next_id += 1
    return new_todo

@router.get("/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int):
    """특정 ID의 Todo를 조회합니다."""
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    return todo

@router.put("/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate):
    """특정 ID의 Todo를 수정합니다."""
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    # Pydantic 모델의 update 기능을 활용 (None이 아닌 값만 업데이트)
    update_data = todo_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    
    return todo

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: int):
    """특정 ID의 Todo를 삭제합니다."""
    global todos
    todo = find_todo(todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )
    
    todos = [t for t in todos if t.id != todo_id]
    # 204 No Content는 본문을 반환하지 않음
    return

```

\</details\>

\<details\>
\<summary\>💡 필요한 의존성 (pyproject.toml)\</summary\>

pyproject.toml의 `dependencies` 섹션:

```toml
dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.24.0",
]
```

\</details\>

-----

이런 현상은 보통 파일을 저장하거나 열 때 인코딩(캐릭터셋)이 잘못 지정되어 발생합니다. (예: UTF-8로 저장된 파일을 EUC-KR로 읽는 경우)

파일을 저장하실 때 인코딩 형식을 **UTF-8**로 설정하시면 이런 문제를 예방할 수 있습니다.

혹시 이 코드 내용 중에서 궁금한 점이 있으신가요?