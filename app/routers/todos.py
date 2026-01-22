from fastapi import APIRouter, HTTPException, status
from typing import List
from ..models import Todo, TodoCreate, TodoUpdate

router = APIRouter()

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
    todos.remove(todo)
    return