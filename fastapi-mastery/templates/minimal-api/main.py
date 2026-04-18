#!/usr/bin/env python3
"""
🔰 Minimal FastAPI Template
=========================

최소한의 기능으로 빠른 프로토타이핑을 위한 단일 파일 FastAPI 애플리케이션

특징:
- 단일 파일로 구성
- 기본적인 CRUD 작업
- 간단한 인메모리 저장
- 즉시 실행 가능

사용법:
    python main.py
    또는
    uvicorn main:app --reload
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uvicorn

# 📊 애플리케이션 설정
app = FastAPI(
    title="Minimal API",
    description="빠른 프로토타이핑을 위한 최소 FastAPI 템플릿",
    version="1.0.0",
    docs_url="/",  # Swagger UI를 루트에 배치
)

# 📋 데이터 모델
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="아이템 이름")
    description: Optional[str] = Field(None, max_length=500, description="아이템 설명")
    tags: List[str] = Field(default_factory=list, description="태그 목록")

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None

class Item(ItemBase):
    id: int = Field(..., description="고유 ID")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시간")
    updated_at: datetime = Field(default_factory=datetime.now, description="수정 시간")

# 🗄️ 인메모리 저장소
items_storage: Dict[int, Item] = {}
next_id = 1

# 🛠️ 헬퍼 함수
def find_item(item_id: int) -> Item:
    """ID로 아이템을 찾는 헬퍼 함수"""
    if item_id not in items_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    return items_storage[item_id]

# 🚀 API 엔드포인트

@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """서버 상태 확인"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_items": len(items_storage)
    }

@app.get("/items", response_model=List[Item], tags=["Items"])
async def get_items(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Item]:
    """모든 아이템 조회 (검색 및 페이지네이션 지원)"""
    items = list(items_storage.values())
    
    # 🔍 검색 필터
    if search:
        items = [item for item in items if search.lower() in item.name.lower()]
    
    # 📄 페이지네이션
    return items[skip:skip + limit]

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(item: ItemCreate) -> Item:
    """새 아이템 생성"""
    global next_id
    
    new_item = Item(
        id=next_id,
        **item.model_dump()
    )
    items_storage[next_id] = new_item
    next_id += 1
    
    return new_item

@app.get("/items/{item_id}", response_model=Item, tags=["Items"])
async def get_item(item_id: int) -> Item:
    """특정 아이템 조회"""
    return find_item(item_id)

@app.put("/items/{item_id}", response_model=Item, tags=["Items"])
async def update_item(item_id: int, item_update: ItemUpdate) -> Item:
    """아이템 수정"""
    item = find_item(item_id)
    
    # 📝 제공된 필드만 업데이트
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    item.updated_at = datetime.now()
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(item_id: int):
    """아이템 삭제"""
    if item_id not in items_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found"
        )
    del items_storage[item_id]

@app.get("/stats", tags=["Statistics"])
async def get_statistics() -> Dict[str, Any]:
    """간단한 통계 정보"""
    items = list(items_storage.values())
    
    return {
        "total_items": len(items),
        "items_with_descriptions": len([item for item in items if item.description]),
        "total_tags": len(set(tag for item in items for tag in item.tags)),
        "most_common_tags": _get_most_common_tags(items, top=5)
    }

def _get_most_common_tags(items: List[Item], top: int = 5) -> List[Dict[str, Any]]:
    """가장 많이 사용된 태그 조회"""
    tag_counts = {}
    for item in items:
        for tag in item.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    # 사용 빈도순으로 정렬
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    return [{"tag": tag, "count": count} for tag, count in sorted_tags[:top]]

# 🎯 예제 데이터 추가 (선택사항)
@app.on_event("startup")
async def add_sample_data():
    """시작 시 예제 데이터 추가"""
    sample_items = [
        ItemCreate(
            name="FastAPI 학습",
            description="FastAPI 프레임워크 완전 정복하기",
            tags=["python", "api", "web"]
        ),
        ItemCreate(
            name="프로젝트 기획",
            description="새로운 웹 서비스 아이디어 구상",
            tags=["planning", "idea"]
        ),
        ItemCreate(
            name="코드 리뷰",
            description="팀 프로젝트 코드 검토",
            tags=["review", "team", "quality"]
        )
    ]
    
    global next_id
    for sample in sample_items:
        new_item = Item(id=next_id, **sample.model_dump())
        items_storage[next_id] = new_item
        next_id += 1

# 🏃‍♂️ 직접 실행
if __name__ == "__main__":
    print("🚀 Minimal FastAPI Template Starting...")
    print("📖 API 문서: http://localhost:8000/")
    print("⚡ API 엔드포인트: http://localhost:8000/items")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["."],
    )