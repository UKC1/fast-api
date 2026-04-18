import json
import time
from typing import Dict, Any, List
from fastapi import APIRouter, Response
from pydantic import BaseModel
from datetime import datetime
from ..observability import get_logger

try:
    import orjson
    ORJSON_AVAILABLE = True
except ImportError:
    ORJSON_AVAILABLE = False

try:
    import ujson
    UJSON_AVAILABLE = True
except ImportError:
    UJSON_AVAILABLE = False

try:
    import msgpack
    MSGPACK_AVAILABLE = True
except ImportError:
    MSGPACK_AVAILABLE = False

router = APIRouter(prefix="/json", tags=["json-comparison"])
logger = get_logger("json_comparison")

class TestData(BaseModel):
    id: int
    name: str
    email: str
    age: int
    address: Dict[str, str]
    tags: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    is_active: bool

def generate_test_data(count: int = 100) -> List[Dict[str, Any]]:
    data = []
    for i in range(count):
        data.append({
            "id": i,
            "name": f"User {i}",
            "email": f"user{i}@example.com",
            "age": 20 + (i % 50),
            "address": {
                "street": f"{i} Main St",
                "city": f"City {i % 10}",
                "country": "USA",
                "postal_code": f"{10000 + i}"
            },
            "tags": [f"tag{j}" for j in range(i % 5 + 1)],
            "metadata": {
                "login_count": i * 10,
                "last_login": datetime.utcnow().isoformat(),
                "preferences": {
                    "theme": "dark" if i % 2 == 0 else "light",
                    "notifications": True if i % 3 == 0 else False
                }
            },
            "created_at": datetime.utcnow().isoformat(),
            "is_active": i % 2 == 0
        })
    return data

@router.get("/standard/{count}")
async def test_standard_json(count: int = 100):
    data = generate_test_data(count)
    
    start_encode = time.perf_counter()
    encoded = json.dumps(data)
    encode_time = (time.perf_counter() - start_encode) * 1000
    
    start_decode = time.perf_counter()
    decoded = json.loads(encoded)
    decode_time = (time.perf_counter() - start_decode) * 1000
    
    logger.info(
        "Standard JSON performance",
        extra={
            "performance": {
                "library": "json",
                "encode_ms": round(encode_time, 3),
                "decode_ms": round(decode_time, 3),
                "data_size": len(encoded),
                "record_count": count
            }
        }
    )
    
    return {
        "library": "standard json",
        "performance": {
            "encode_ms": round(encode_time, 3),
            "decode_ms": round(decode_time, 3),
            "total_ms": round(encode_time + decode_time, 3),
            "data_size_bytes": len(encoded),
            "record_count": count
        },
        "sample_data": decoded[:3]
    }

@router.get("/orjson/{count}")
async def test_orjson(count: int = 100):
    if not ORJSON_AVAILABLE:
        return {"error": "orjson not installed. Run: pip install orjson"}
    
    data = generate_test_data(count)
    
    start_encode = time.perf_counter()
    encoded = orjson.dumps(data)
    encode_time = (time.perf_counter() - start_encode) * 1000
    
    start_decode = time.perf_counter()
    decoded = orjson.loads(encoded)
    decode_time = (time.perf_counter() - start_decode) * 1000
    
    logger.info(
        "orjson performance",
        extra={
            "performance": {
                "library": "orjson",
                "encode_ms": round(encode_time, 3),
                "decode_ms": round(decode_time, 3),
                "data_size": len(encoded),
                "record_count": count
            }
        }
    )
    
    return {
        "library": "orjson",
        "performance": {
            "encode_ms": round(encode_time, 3),
            "decode_ms": round(decode_time, 3),
            "total_ms": round(encode_time + decode_time, 3),
            "data_size_bytes": len(encoded),
            "record_count": count
        },
        "sample_data": decoded[:3]
    }

@router.get("/ujson/{count}")
async def test_ujson(count: int = 100):
    if not UJSON_AVAILABLE:
        return {"error": "ujson not installed. Run: pip install ujson"}
    
    data = generate_test_data(count)
    
    start_encode = time.perf_counter()
    encoded = ujson.dumps(data)
    encode_time = (time.perf_counter() - start_encode) * 1000
    
    start_decode = time.perf_counter()
    decoded = ujson.loads(encoded)
    decode_time = (time.perf_counter() - start_decode) * 1000
    
    logger.info(
        "ujson performance",
        extra={
            "performance": {
                "library": "ujson",
                "encode_ms": round(encode_time, 3),
                "decode_ms": round(decode_time, 3),
                "data_size": len(encoded),
                "record_count": count
            }
        }
    )
    
    return {
        "library": "ujson",
        "performance": {
            "encode_ms": round(encode_time, 3),
            "decode_ms": round(decode_time, 3),
            "total_ms": round(encode_time + decode_time, 3),
            "data_size_bytes": len(encoded),
            "record_count": count
        },
        "sample_data": decoded[:3]
    }

@router.get("/msgpack/{count}")
async def test_msgpack(count: int = 100):
    if not MSGPACK_AVAILABLE:
        return {"error": "msgpack not installed. Run: pip install msgpack"}
    
    data = generate_test_data(count)
    
    start_encode = time.perf_counter()
    encoded = msgpack.packb(data, use_bin_type=True)
    encode_time = (time.perf_counter() - start_encode) * 1000
    
    start_decode = time.perf_counter()
    decoded = msgpack.unpackb(encoded, raw=False)
    decode_time = (time.perf_counter() - start_decode) * 1000
    
    logger.info(
        "msgpack performance",
        extra={
            "performance": {
                "library": "msgpack",
                "encode_ms": round(encode_time, 3),
                "decode_ms": round(decode_time, 3),
                "data_size": len(encoded),
                "record_count": count
            }
        }
    )
    
    return {
        "library": "msgpack",
        "performance": {
            "encode_ms": round(encode_time, 3),
            "decode_ms": round(decode_time, 3),
            "total_ms": round(encode_time + decode_time, 3),
            "data_size_bytes": len(encoded),
            "record_count": count
        },
        "sample_data": decoded[:3]
    }

@router.get("/compare/{count}")
async def compare_all(count: int = 100):
    results = {}
    
    data = generate_test_data(count)
    
    start = time.perf_counter()
    json_encoded = json.dumps(data)
    json_encode_time = (time.perf_counter() - start) * 1000
    
    start = time.perf_counter()
    json_decoded = json.loads(json_encoded)
    json_decode_time = (time.perf_counter() - start) * 1000
    
    results["json"] = {
        "encode_ms": round(json_encode_time, 3),
        "decode_ms": round(json_decode_time, 3),
        "total_ms": round(json_encode_time + json_decode_time, 3),
        "size_bytes": len(json_encoded)
    }
    
    if ORJSON_AVAILABLE:
        start = time.perf_counter()
        orjson_encoded = orjson.dumps(data)
        orjson_encode_time = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        orjson_decoded = orjson.loads(orjson_encoded)
        orjson_decode_time = (time.perf_counter() - start) * 1000
        
        results["orjson"] = {
            "encode_ms": round(orjson_encode_time, 3),
            "decode_ms": round(orjson_decode_time, 3),
            "total_ms": round(orjson_encode_time + orjson_decode_time, 3),
            "size_bytes": len(orjson_encoded),
            "speedup_vs_json": round(json_encode_time / orjson_encode_time, 2) if orjson_encode_time > 0 else 0
        }
    
    if UJSON_AVAILABLE:
        start = time.perf_counter()
        ujson_encoded = ujson.dumps(data)
        ujson_encode_time = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        ujson_decoded = ujson.loads(ujson_encoded)
        ujson_decode_time = (time.perf_counter() - start) * 1000
        
        results["ujson"] = {
            "encode_ms": round(ujson_encode_time, 3),
            "decode_ms": round(ujson_decode_time, 3),
            "total_ms": round(ujson_encode_time + ujson_decode_time, 3),
            "size_bytes": len(ujson_encoded),
            "speedup_vs_json": round(json_encode_time / ujson_encode_time, 2) if ujson_encode_time > 0 else 0,
            "compression_ratio": round(len(json_encoded) / len(ujson_encoded), 2) if len(ujson_encoded) > 0 else 0
        }
    
    # Debug log
    logger.info(f"MSGPACK_AVAILABLE: {MSGPACK_AVAILABLE}")
    
    if MSGPACK_AVAILABLE:
        start = time.perf_counter()
        msgpack_encoded = msgpack.packb(data, use_bin_type=True)
        msgpack_encode_time = (time.perf_counter() - start) * 1000
        
        start = time.perf_counter()
        msgpack_decoded = msgpack.unpackb(msgpack_encoded, raw=False)
        msgpack_decode_time = (time.perf_counter() - start) * 1000
        
        results["msgpack"] = {
            "encode_ms": round(msgpack_encode_time, 3),
            "decode_ms": round(msgpack_decode_time, 3),
            "total_ms": round(msgpack_encode_time + msgpack_decode_time, 3),
            "size_bytes": len(msgpack_encoded),
            "speedup_vs_json": round(json_encode_time / msgpack_encode_time, 2) if msgpack_encode_time > 0 else 0,
            "compression_ratio": round(len(json_encoded) / len(msgpack_encoded), 2)
        }
    
    logger.info(
        "JSON library comparison",
        extra={
            "performance": results,
            "extra_data": {
                "record_count": count
            }
        }
    )
    
    return {
        "record_count": count,
        "comparison": results,
        "fastest_encoder": min(results.items(), key=lambda x: x[1]["encode_ms"])[0],
        "fastest_decoder": min(results.items(), key=lambda x: x[1]["decode_ms"])[0],
        "fastest_overall": min(results.items(), key=lambda x: x[1]["total_ms"])[0]
    }