"""
JSON 직렬화 성능 비교 데모
실제로 왜 직렬화가 느린지, 어떻게 개선되는지 보여주는 예제
"""

import json
import time
import sys
from typing import List, Dict, Any
import orjson
import ujson

def create_test_data(size: int = 1000) -> List[Dict[str, Any]]:
    """테스트용 복잡한 데이터 구조 생성"""
    return [
        {
            "id": i,
            "user": {
                "name": f"사용자_{i}",
                "email": f"user{i}@example.com",
                "profile": {
                    "age": 20 + (i % 50),
                    "interests": [f"관심사_{j}" for j in range(5)],
                    "scores": {
                        "math": 70 + (i % 30),
                        "english": 60 + (i % 40),
                        "science": 80 + (i % 20)
                    }
                }
            },
            "transactions": [
                {
                    "id": f"tx_{i}_{j}",
                    "amount": 1000 * j,
                    "timestamp": f"2024-01-{j:02d}T10:00:00Z"
                }
                for j in range(10)
            ],
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T00:00:00Z",
                "tags": [f"tag_{k}" for k in range(3)],
                "flags": {
                    "is_active": i % 2 == 0,
                    "is_premium": i % 3 == 0,
                    "is_verified": i % 5 == 0
                }
            }
        }
        for i in range(size)
    ]

def measure_performance(name: str, encode_func, decode_func, data: Any) -> Dict[str, float]:
    """성능 측정 헬퍼 함수"""
    
    # 인코딩 측정
    start = time.perf_counter()
    encoded = encode_func(data)
    encode_time = (time.perf_counter() - start) * 1000
    
    # 디코딩 측정
    start = time.perf_counter()
    decoded = decode_func(encoded)
    decode_time = (time.perf_counter() - start) * 1000
    
    return {
        "library": name,
        "encode_ms": round(encode_time, 2),
        "decode_ms": round(decode_time, 2),
        "total_ms": round(encode_time + decode_time, 2),
        "size_bytes": len(encoded) if isinstance(encoded, (str, bytes)) else 0
    }

def visualize_results(results: List[Dict[str, float]]):
    """결과를 시각적으로 표현"""
    print("\n" + "="*60)
    print("JSON 라이브러리 성능 비교 결과")
    print("="*60)
    
    # 헤더 출력
    print(f"{'라이브러리':<12} {'인코딩(ms)':<12} {'디코딩(ms)':<12} {'총시간(ms)':<12} {'크기(bytes)':<12}")
    print("-"*60)
    
    # 결과 출력
    for r in results:
        print(f"{r['library']:<12} {r['encode_ms']:<12} {r['decode_ms']:<12} {r['total_ms']:<12} {r['size_bytes']:<12}")
    
    # 최적 라이브러리 찾기
    fastest_encode = min(results, key=lambda x: x['encode_ms'])
    fastest_decode = min(results, key=lambda x: x['decode_ms'])
    fastest_total = min(results, key=lambda x: x['total_ms'])
    smallest_size = min(results, key=lambda x: x['size_bytes'])
    
    print("\n" + "="*60)
    print("성능 우승자")
    print("="*60)
    print(f"가장 빠른 인코딩: {fastest_encode['library']} ({fastest_encode['encode_ms']}ms)")
    print(f"가장 빠른 디코딩: {fastest_decode['library']} ({fastest_decode['decode_ms']}ms)")
    print(f"가장 빠른 전체: {fastest_total['library']} ({fastest_total['total_ms']}ms)")
    print(f"가장 작은 크기: {smallest_size['library']} ({smallest_size['size_bytes']:,} bytes)")
    
    # 표준 대비 성능 향상
    standard = next((r for r in results if r['library'] == 'json'), None)
    if standard:
        print("\n" + "="*60)
        print("표준 json 대비 성능 향상")
        print("="*60)
        for r in results:
            if r['library'] != 'json':
                speedup = round(standard['total_ms'] / r['total_ms'], 2)
                print(f"{r['library']}: {speedup}x 빠름")

def demonstrate_why_slow():
    """왜 표준 JSON이 느린지 설명하는 데모"""
    print("\n" + "="*60)
    print("왜 표준 JSON이 느린가?")
    print("="*60)
    
    test_obj = {
        "numbers": list(range(1000)),
        "strings": [f"문자열_{i}" for i in range(100)],
        "nested": {
            "level1": {
                "level2": {
                    "level3": "깊은 중첩"
                }
            }
        }
    }
    
    print("\n1. 타입 검사 오버헤드:")
    print("   - Python은 모든 객체의 타입을 런타임에 확인")
    print("   - 재귀적으로 모든 요소를 순회하며 JSON 호환성 검사")
    
    start = time.perf_counter()
    for _ in range(1000):
        isinstance(test_obj, dict)
        for key in test_obj:
            isinstance(test_obj[key], (list, dict, str, int, float, bool, type(None)))
    type_check_time = (time.perf_counter() - start) * 1000
    print(f"   → 1000번 타입 체크: {type_check_time:.2f}ms")
    
    print("\n2. 문자열 조작 비효율:")
    print("   - Python 문자열은 불변(immutable)")
    print("   - 매번 새로운 문자열 객체 생성")
    
    start = time.perf_counter()
    result = ""
    for i in range(1000):
        result += f"item_{i},"  # 매번 새 문자열 생성
    string_concat_time = (time.perf_counter() - start) * 1000
    print(f"   → 1000번 문자열 연결: {string_concat_time:.2f}ms")
    
    print("\n3. GIL (Global Interpreter Lock):")
    print("   - 한 번에 하나의 Python 바이트코드만 실행")
    print("   - 멀티코어 활용 불가")
    
    print("\n4. C/Rust 라이브러리의 해결책:")
    print("   - 타입 검사를 네이티브 코드로 처리")
    print("   - 효율적인 메모리 할당과 문자열 버퍼")
    print("   - GIL 우회 가능")

def main():
    """메인 실행 함수"""
    print("JSON 직렬화 성능 테스트 시작...")
    print(f"Python 버전: {sys.version}")
    
    # 데이터 크기별 테스트
    test_sizes = [100, 1000, 5000]
    
    for size in test_sizes:
        print(f"\n{'='*60}")
        print(f"테스트 데이터 크기: {size} 레코드")
        print('='*60)
        
        data = create_test_data(size)
        results = []
        
        # 표준 json
        results.append(measure_performance(
            "json",
            json.dumps,
            json.loads,
            data
        ))
        
        # orjson
        results.append(measure_performance(
            "orjson",
            lambda d: orjson.dumps(d),
            lambda s: orjson.loads(s),
            data
        ))
        
        # ujson
        results.append(measure_performance(
            "ujson",
            ujson.dumps,
            ujson.loads,
            data
        ))
        
        visualize_results(results)
    
    # 추가 설명
    demonstrate_why_slow()
    
    print("\n" + "="*60)
    print("실무 적용 가이드")
    print("="*60)
    print("""
1. 일반 웹 API: orjson 사용 (4-7배 빠름)
   from fastapi.responses import ORJSONResponse
   
2. 데이터 분석: ujson 사용 (pandas 호환)
   df.to_json(orient='records', force_ascii=False)
   
3. 마이크로서비스: msgpack 고려 (바이너리, 30% 작음)
   import msgpack
   
4. 설정 파일: 표준 json 사용 (호환성)
   with open('config.json') as f:
       config = json.load(f)
    """)

if __name__ == "__main__":
    main()