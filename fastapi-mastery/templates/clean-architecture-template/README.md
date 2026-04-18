# 🏛️ Clean Architecture FastAPI Template

> **목표**: Clean Architecture 원칙을 적용한 확장 가능하고 테스트 가능한 FastAPI 애플리케이션

## 🎯 아키텍처 철학

**"비즈니스 로직을 프레임워크로부터 독립시켜라"**

이 템플릿은 Uncle Bob의 Clean Architecture 원칙을 FastAPI에 적용하여 다음을 달성합니다:

- ✅ **독립성**: 비즈니스 로직이 프레임워크에 의존하지 않음
- ✅ **테스트성**: 모든 계층을 독립적으로 테스트 가능
- ✅ **유연성**: 데이터베이스나 프레임워크 교체 용이
- ✅ **확장성**: 새로운 기능 추가가 기존 코드에 영향 최소

## 🏗️ 아키텍처 구조

```
🌐 Presentation Layer (FastAPI)
    ↓ (의존성 방향)
💼 Application Layer (Use Cases)
    ↓
🏢 Domain Layer (Business Logic)
    ↓
🗄️ Infrastructure Layer (Database/External APIs)
```

### 📁 디렉토리 구조
```
src/
├── presentation/           # 🌐 프레젠테이션 계층
│   ├── api/               # FastAPI 라우터
│   ├── schemas/           # Pydantic 스키마
│   └── middleware/        # 미들웨어
│
├── application/           # 💼 애플리케이션 계층  
│   ├── use_cases/         # 비즈니스 유스케이스
│   └── interfaces/        # 추상 인터페이스
│
├── domain/               # 🏢 도메인 계층
│   ├── entities/         # 비즈니스 엔티티
│   ├── value_objects/    # 값 객체
│   └── events/          # 도메인 이벤트
│
└── infrastructure/       # 🗄️ 인프라스트럭처 계층
    ├── database/         # 데이터베이스 구현
    ├── external_apis/    # 외부 API 연동
    └── services/        # 외부 서비스
```

## 🚀 빠른 시작

### 1. 프로젝트 생성
```bash
# 템플릿 복사
cp -r templates/clean-architecture-template my-clean-project
cd my-clean-project

# 가상환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate
```

### 2. 의존성 설치
```bash
# UV 사용 (권장)
uv install

# 또는 pip 사용
pip install -r requirements.txt
```

### 3. 데이터베이스 초기화
```bash
# 데이터베이스 설정
python scripts/init_db.py

# 마이그레이션 실행
alembic upgrade head
```

### 4. 서버 실행
```bash
# 개발 서버
uvicorn src.presentation.main:app --reload

# 또는 스크립트 사용
python scripts/run_dev.py
```

## 🧩 계층별 설명

### 🏢 Domain Layer (도메인 계층)
**역할**: 순수한 비즈니스 로직, 외부 의존성 없음

```python
# src/domain/entities/user.py
from dataclasses import dataclass
from typing import Optional
from src.domain.value_objects import Email, UserId

@dataclass
class User:
    id: UserId
    email: Email
    name: str
    is_active: bool = True
    
    def activate(self) -> None:
        """사용자 활성화 비즈니스 로직"""
        if not self.is_active:
            self.is_active = True
            # 도메인 이벤트 발생
            DomainEvents.raise(UserActivated(self.id))
    
    def can_create_post(self) -> bool:
        """게시글 생성 가능 여부"""
        return self.is_active
```

### 💼 Application Layer (애플리케이션 계층)
**역할**: 유스케이스 조합, 도메인 객체 활용

```python
# src/application/use_cases/create_user.py
from src.domain.entities import User
from src.domain.value_objects import Email, UserId
from src.application.interfaces import UserRepository, EmailService

class CreateUserUseCase:
    def __init__(
        self, 
        user_repo: UserRepository,
        email_service: EmailService
    ):
        self._user_repo = user_repo
        self._email_service = email_service
    
    async def execute(self, email: str, name: str) -> User:
        # 비즈니스 룰 검증
        if await self._user_repo.exists_by_email(Email(email)):
            raise UserAlreadyExistsError(email)
        
        # 도메인 객체 생성
        user = User(
            id=UserId.generate(),
            email=Email(email),
            name=name
        )
        
        # 저장
        await self._user_repo.save(user)
        
        # 외부 서비스 호출
        await self._email_service.send_welcome_email(user)
        
        return user
```

### 🌐 Presentation Layer (프레젠테이션 계층)
**역할**: HTTP 요청/응답 처리, FastAPI 라우팅

```python
# src/presentation/api/users.py
from fastapi import APIRouter, Depends, status
from src.presentation.schemas import CreateUserRequest, UserResponse
from src.application.use_cases import CreateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Depends(get_create_user_use_case)
) -> UserResponse:
    """새 사용자 생성"""
    user = await use_case.execute(request.email, request.name)
    return UserResponse.from_domain(user)
```

### 🗄️ Infrastructure Layer (인프라스트럭처 계층)
**역할**: 외부 시스템 연동, 구체적 구현

```python
# src/infrastructure/database/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from src.application.interfaces import UserRepository
from src.domain.entities import User

class SQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def save(self, user: User) -> None:
        db_user = UserModel.from_domain(user)
        self._session.add(db_user)
        await self._session.commit()
    
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id.value)
        )
        db_user = result.scalar_one_or_none()
        return db_user.to_domain() if db_user else None
```

## 🧪 테스트 전략

### 계층별 테스트 접근법

#### 1. Domain Layer 테스트 (Unit Tests)
```python
# tests/unit/domain/test_user.py
def test_user_activation():
    # Given
    user = User(id=UserId("123"), email=Email("test@test.com"), name="Test", is_active=False)
    
    # When
    user.activate()
    
    # Then
    assert user.is_active == True
```

#### 2. Application Layer 테스트 (Unit Tests with Mocks)
```python
# tests/unit/application/test_create_user.py
@pytest.mark.asyncio
async def test_create_user_success():
    # Given
    user_repo = Mock(spec=UserRepository)
    email_service = Mock(spec=EmailService)
    use_case = CreateUserUseCase(user_repo, email_service)
    
    user_repo.exists_by_email.return_value = False
    
    # When
    result = await use_case.execute("test@test.com", "Test User")
    
    # Then
    assert result.email.value == "test@test.com"
    user_repo.save.assert_called_once()
    email_service.send_welcome_email.assert_called_once()
```

#### 3. Integration Tests
```python
# tests/integration/test_user_api.py
@pytest.mark.asyncio
async def test_create_user_api():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/users/", json={
            "email": "test@test.com",
            "name": "Test User"
        })
        assert response.status_code == 201
        assert response.json()["email"] == "test@test.com"
```

## 🔧 의존성 주입

### Container 설정
```python
# src/infrastructure/container.py
from dependency_injector import containers, providers
from src.application.use_cases import CreateUserUseCase
from src.infrastructure.database import SQLUserRepository

class Container(containers.DeclarativeContainer):
    # Database
    db_session = providers.Factory(get_db_session)
    
    # Repositories  
    user_repository = providers.Factory(
        SQLUserRepository,
        session=db_session
    )
    
    # Use Cases
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repo=user_repository,
        email_service=email_service
    )
```

## 📊 프로젝트 예시

### 블로그 플랫폼
```
Domain:
- User (사용자)
- Post (게시글)  
- Comment (댓글)
- Tag (태그)

Use Cases:
- CreateUser (사용자 생성)
- PublishPost (게시글 발행)
- AddComment (댓글 추가)
- FollowUser (사용자 팔로우)
```

### 이커머스
```
Domain:
- Customer (고객)
- Product (상품)
- Order (주문)
- Inventory (재고)

Use Cases:
- PlaceOrder (주문 생성)
- ProcessPayment (결제 처리)
- UpdateInventory (재고 업데이트)
- CalculateShipping (배송비 계산)
```

## 🎯 베스트 프랙티스

### 1. 의존성 방향 준수
```
Presentation → Application → Domain ← Infrastructure
```

### 2. 인터페이스 우선 설계
```python
# 먼저 인터페이스 정의
class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None: pass

# 나중에 구현체 작성
class SQLUserRepository(UserRepository):
    async def save(self, user: User) -> None:
        # 구체적 구현
```

### 3. 도메인 이벤트 활용
```python
# 도메인 로직에서 이벤트 발생
user.activate()  # UserActivated 이벤트 발생

# 애플리케이션 레이어에서 이벤트 처리
@event_handler(UserActivated)
async def send_welcome_email(event: UserActivated):
    # 환영 이메일 발송
```

## 📈 확장 가이드

### 새 기능 추가 절차
1. **Domain**: 엔티티/값 객체 정의
2. **Application**: 유스케이스 구현
3. **Infrastructure**: 저장소/서비스 구현
4. **Presentation**: API 엔드포인트 추가
5. **Tests**: 각 계층별 테스트 작성

---

**🎯 Clean Architecture로 견고하고 유연한 FastAPI 애플리케이션을 구축해보세요!**