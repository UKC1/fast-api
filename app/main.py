from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .routers import todos

app = FastAPI(
    title="Basic Todo List API",
    description="FastAPI 튜토리얼을 위한 기본 TODO 리스트 API입니다.",
    version="0.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 구체적인 도메인 설정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# /todos 접두사와 "todos" 태그로 라우터 포함
app.include_router(todos.router, prefix="/todos", tags=["todos"])

# 정적 파일 서빙 설정
app.mount("/static", StaticFiles(directory="frontend/src"), name="static")

@app.get("/")
async def root():
    return {"message": "Welcome to Basic Todo List API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)