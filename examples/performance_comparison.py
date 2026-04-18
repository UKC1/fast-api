from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import time
import json
import orjson

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str
    metadata: Dict[str, Any]

# Case 1: Pydantic + Standard JSON (가장 느림)
@app.get("/slow")
async def slow_endpoint():
    data = {"id": 1, "name": "John", "email": "john@test.com", "metadata": {}}
    
    # Pydantic validation (느림)
    start = time.perf_counter()
    user = User(**data)  
    pydantic_time = (time.perf_counter() - start) * 1000
    
    # Standard JSON serialization (느림)
    start = time.perf_counter()
    json_str = json.dumps(user.model_dump())
    json_time = (time.perf_counter() - start) * 1000
    
    return {
        "pydantic_ms": pydantic_time,
        "json_ms": json_time,
        "total_ms": pydantic_time + json_time
    }

# Case 2: Pydantic + orjson (중간)
@app.get("/medium")
async def medium_endpoint():
    data = {"id": 1, "name": "John", "email": "john@test.com", "metadata": {}}
    
    # Pydantic validation (여전히 느림)
    start = time.perf_counter()
    user = User(**data)
    pydantic_time = (time.perf_counter() - start) * 1000
    
    # orjson serialization (빠름)
    start = time.perf_counter()
    json_bytes = orjson.dumps(user.model_dump())
    orjson_time = (time.perf_counter() - start) * 1000
    
    return {
        "pydantic_ms": pydantic_time,
        "json_ms": orjson_time,
        "total_ms": pydantic_time + orjson_time
    }

# Case 3: No Pydantic + orjson (가장 빠름)
@app.get("/fast")
async def fast_endpoint():
    data = {"id": 1, "name": "John", "email": "john@test.com", "metadata": {}}
    
    # No validation (매우 빠름)
    start = time.perf_counter()
    # 검증 없음
    no_validation_time = 0
    
    # orjson serialization (빠름)
    start = time.perf_counter()
    json_bytes = orjson.dumps(data)
    orjson_time = (time.perf_counter() - start) * 1000
    
    return {
        "pydantic_ms": no_validation_time,
        "json_ms": orjson_time,
        "total_ms": orjson_time
    }