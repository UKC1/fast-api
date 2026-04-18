"""
FastAPI에서 JSON 라이브러리 최적화 실전 예제
Pydantic과 orjson을 함께 사용하여 최고 성능 달성
"""

from fastapi import FastAPI, Response
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import orjson
import time
from functools import lru_cache

# ========================
# 1. 최적화된 Pydantic 모델
# ========================

class OptimizedConfig:
    """재사용 가능한 최적화 설정"""
    model_config = ConfigDict(
        # 검증 최소화
        validate_assignment=False,
        use_enum_values=True,
        arbitrary_types_allowed=False,
        # 성능 향상
        str_strip_whitespace=True,
        # JSON 스키마 캐싱
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "홍길동"
            }
        }
    )

class User(BaseModel, OptimizedConfig):
    """최적화된 사용자 모델"""
    id: int
    name: str
    email: str
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Product(BaseModel, OptimizedConfig):
    """최적화된 상품 모델"""
    id: int
    name: str
    price: float
    stock: int
    tags: List[str] = Field(default_factory=list)

# ========================
# 2. 커스텀 응답 클래스
# ========================

class OptimizedORJSONResponse(ORJSONResponse):
    """최적화된 orjson 응답 클래스"""
    
    def render(self, content: Any) -> bytes:
        # orjson 옵션 플래그
        # OPT_SERIALIZE_NUMPY: numpy 배열 지원
        # OPT_SERIALIZE_UUID: UUID 자동 변환
        # OPT_NON_STR_KEYS: 문자열이 아닌 딕셔너리 키 허용
        return orjson.dumps(
            content,
            option=(
                orjson.OPT_NON_STR_KEYS |
                orjson.OPT_SERIALIZE_UUID |
                orjson.OPT_INDENT_2  # 개발 환경에서는 가독성
            )
        )

# ========================
# 3. FastAPI 앱 설정
# ========================

app = FastAPI(
    title="고성능 API",
    default_response_class=OptimizedORJSONResponse,
    # Swagger UI에서도 빠른 렌더링
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

# ========================
# 4. 성능 측정 미들웨어
# ========================

@app.middleware("http")
async def add_process_time_header(request, call_next):
    """응답 시간 측정"""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-ms"] = str(round(process_time, 2))
    return response

# ========================
# 5. 캐싱 전략
# ========================

@lru_cache(maxsize=128)
def get_cached_products(category: str, limit: int) -> bytes:
    """자주 요청되는 데이터는 직렬화된 상태로 캐싱"""
    products = [
        {"id": i, "name": f"상품_{i}", "category": category, "price": i * 1000}
        for i in range(limit)
    ]
    return orjson.dumps(products)

@app.get("/cached/products")
async def get_products_cached(category: str = "전자제품", limit: int = 100):
    """캐시된 상품 목록"""
    return Response(
        content=get_cached_products(category, limit),
        media_type="application/json"
    )

# ========================
# 6. 스트리밍 응답
# ========================

async def generate_large_dataset():
    """대용량 데이터를 스트리밍으로 전송"""
    for batch in range(100):
        data = [
            {"id": i, "value": i * 2, "batch": batch}
            for i in range(100)
        ]
        yield orjson.dumps(data) + b"\n"

@app.get("/stream/data")
async def stream_large_data():
    """NDJSON (Newline Delimited JSON) 스트리밍"""
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        generate_large_dataset(),
        media_type="application/x-ndjson"
    )

# ========================
# 7. 벤치마크 엔드포인트
# ========================

@app.get("/benchmark/serialization")
async def benchmark_serialization(records: int = 1000):
    """직렬화 성능 비교"""
    import json
    
    # 테스트 데이터 생성
    data = [
        {
            "id": i,
            "name": f"사용자_{i}",
            "email": f"user{i}@test.com",
            "created_at": datetime.now().isoformat(),
            "metadata": {"score": i * 10, "level": i % 10}
        }
        for i in range(records)
    ]
    
    # Pydantic 모델 생성 시간
    start = time.perf_counter()
    users = [User(**d) for d in data]
    pydantic_time = (time.perf_counter() - start) * 1000
    
    # Pydantic → dict 변환
    start = time.perf_counter()
    user_dicts = [u.model_dump() for u in users]
    dict_time = (time.perf_counter() - start) * 1000
    
    # 표준 JSON
    start = time.perf_counter()
    json_str = json.dumps(user_dicts, default=str)
    json_time = (time.perf_counter() - start) * 1000
    
    # orjson
    start = time.perf_counter()
    orjson_bytes = orjson.dumps(user_dicts)
    orjson_time = (time.perf_counter() - start) * 1000
    
    return {
        "records": records,
        "times_ms": {
            "pydantic_validation": round(pydantic_time, 2),
            "model_to_dict": round(dict_time, 2),
            "json_serialization": round(json_time, 2),
            "orjson_serialization": round(orjson_time, 2),
            "total_standard": round(pydantic_time + dict_time + json_time, 2),
            "total_optimized": round(pydantic_time + dict_time + orjson_time, 2)
        },
        "speedup": {
            "serialization_only": round(json_time / orjson_time, 2),
            "total": round(
                (pydantic_time + dict_time + json_time) /
                (pydantic_time + dict_time + orjson_time),
                2
            )
        },
        "sizes": {
            "json_bytes": len(json_str.encode()),
            "orjson_bytes": len(orjson_bytes)
        }
    }

@app.get("/benchmark/response-models")
async def benchmark_response_models(use_response_model: bool = True):
    """response_model 사용 vs 미사용 비교"""
    data = [{"id": i, "name": f"User_{i}"} for i in range(1000)]
    
    if use_response_model:
        # Pydantic 검증 있음 (느림)
        @app.get("/temp/with-model", response_model=List[User])
        async def with_model():
            return data
        return {"mode": "with_response_model", "data": data[:5]}
    else:
        # Pydantic 검증 없음 (빠름)
        return {"mode": "without_response_model", "data": data[:5]}

# ========================
# 8. 실무 최적화 패턴
# ========================

class DatabaseResult:
    """DB 결과를 직접 JSON으로 변환"""
    
    @staticmethod
    def to_json(rows: List[tuple], columns: List[str]) -> bytes:
        """SQL 결과를 바로 JSON으로 (Pydantic 우회)"""
        result = [
            dict(zip(columns, row))
            for row in rows
        ]
        return orjson.dumps(result)

@app.get("/optimized/database")
async def optimized_database_query():
    """최적화된 데이터베이스 쿼리 예제"""
    # 실제로는 DB에서 가져옴
    mock_rows = [(i, f"name_{i}", f"email_{i}@test.com") for i in range(100)]
    mock_columns = ["id", "name", "email"]
    
    # Pydantic 검증 없이 바로 JSON
    json_bytes = DatabaseResult.to_json(mock_rows, mock_columns)
    
    return Response(
        content=json_bytes,
        media_type="application/json"
    )

# ========================
# 9. 조건부 직렬화
# ========================

@app.get("/smart/users")
async def get_users_smart(
    format: str = "json",  # json, compact, full
    validate: bool = True
):
    """요청에 따라 다른 직렬화 전략 사용"""
    data = [
        {"id": i, "name": f"User_{i}", "email": f"u{i}@test.com", "meta": {}}
        for i in range(100)
    ]
    
    if format == "compact":
        # 최소 데이터만 전송
        compact = [{"id": d["id"], "name": d["name"]} for d in data]
        return OptimizedORJSONResponse(compact)
    
    elif format == "full" and validate:
        # 전체 검증과 함께
        users = [User(**d, created_at=datetime.now(), metadata={}) for d in data]
        return [u.model_dump() for u in users]
    
    else:
        # 검증 없이 빠르게
        return OptimizedORJSONResponse(data)

# ========================
# 10. 성능 모니터링
# ========================

@app.get("/health/performance")
async def health_check():
    """API 성능 상태 체크"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    
    return {
        "status": "healthy",
        "performance": {
            "memory_mb": round(process.memory_info().rss / 1024 / 1024, 2),
            "cpu_percent": process.cpu_percent(),
            "num_threads": process.num_threads(),
        },
        "serialization": {
            "default_response_class": "ORJSONResponse",
            "cache_size": get_cached_products.cache_info().currsize,
            "cache_hits": get_cached_products.cache_info().hits,
            "cache_misses": get_cached_products.cache_info().misses,
        }
    }

if __name__ == "__main__":
    import uvicorn
    # 프로덕션 설정
    uvicorn.run(
        "fastapi_optimization:app",
        host="0.0.0.0",
        port=8000,
        # 성능 최적화 설정
        workers=4,  # CPU 코어 수만큼
        loop="uvloop",  # 더 빠른 이벤트 루프
        access_log=False,  # 로깅 오버헤드 제거
    )