import asyncio
import httpx
import statistics
from typing import Dict, List
from tabulate import tabulate
import json

async def run_benchmark():
    """Run performance benchmark"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        test_cases = [10, 100, 1000, 5000, 10000]
        all_results = {}
        
        for count in test_cases:
            print(f"\nTesting {count} records...")
            
            # 5번 반복 측정해서 평균값 사용
            url = f"http://localhost:8080/json/compare/{count}"
            times = []
            
            for _ in range(5):
                response = await client.get(url)
                if response.status_code == 200:
                    times.append(response.json())
            
            if times:
                # 첫 번째 결과를 기준으로 평균 계산
                avg_result = times[0]["comparison"].copy()
                for lib in avg_result:
                    encode_times = [t["comparison"][lib]["encode_ms"] for t in times if lib in t["comparison"]]
                    decode_times = [t["comparison"][lib]["decode_ms"] for t in times if lib in t["comparison"]]
                    
                    avg_result[lib]["encode_ms"] = round(statistics.mean(encode_times), 3)
                    avg_result[lib]["decode_ms"] = round(statistics.mean(decode_times), 3)
                    avg_result[lib]["total_ms"] = round(avg_result[lib]["encode_ms"] + avg_result[lib]["decode_ms"], 3)
                
                all_results[count] = avg_result
        
        return all_results

def generate_report(results: Dict):
    """Generate benchmark report"""
    
    print("\n" + "="*80)
    print("JSON Library Performance Comparison Report")
    print("="*80)
    
    # 라이브러리별 요약
    libraries = ["json", "orjson", "ujson", "msgpack"]
    
    for count, data in results.items():
        print(f"\n### Performance with {count} records")
        
        table_data = []
        for lib in libraries:
            if lib in data:
                row = [
                    lib,
                    f"{data[lib]['encode_ms']:.3f}",
                    f"{data[lib]['decode_ms']:.3f}",
                    f"{data[lib]['total_ms']:.3f}",
                    f"{data[lib]['size_bytes']:,}",
                    f"{data[lib].get('speedup_vs_json', 1):.2f}x"
                ]
                table_data.append(row)
        
        headers = ["Library", "Encode(ms)", "Decode(ms)", "Total(ms)", "Size(bytes)", "Speedup"]
        print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    # 전체 요약
    print("\n" + "="*80)
    print("Production Recommendations")
    print("="*80)
    
    recommendations = """
    1. **orjson** (Best Performance)
       - Pros: Fastest encoding/decoding (3-7x faster than standard)
       - Pros: Automatic datetime, UUID conversion
       - Cons: Not pure Python (Rust-based)
       - Use: High-performance API servers, large data processing
    
    2. **ujson** (Balanced)
       - Pros: Second fastest (2-3x faster than standard)
       - Pros: Widely adopted library
       - Cons: Limited Python type support
       - Use: General web applications
    
    3. **msgpack** (Binary Format)
       - Pros: Smallest data size (20-30% smaller than JSON)
       - Pros: Binary data support
       - Cons: Not human-readable, harder to debug
       - Use: Network bandwidth critical, internal service communication
    
    4. **standard json** (Compatibility)
       - Pros: Standard library, 100% compatibility
       - Pros: No installation required
       - Cons: Slowest performance
       - Use: Small projects, compatibility critical
    """
    
    print(recommendations)
    
    # 성능 순위
    if 10000 in results:
        print("\n### Performance Rankings (10,000 records)")
        data = results[10000]
        
        # 인코딩 속도 순위
        encode_ranking = sorted(
            [(lib, data[lib]["encode_ms"]) for lib in data if lib in libraries],
            key=lambda x: x[1]
        )
        
        print("\nEncoding Speed (fastest first):")
        for i, (lib, time) in enumerate(encode_ranking, 1):
            print(f"  {i}. {lib}: {time:.3f}ms")
        
        # 디코딩 속도 순위  
        decode_ranking = sorted(
            [(lib, data[lib]["decode_ms"]) for lib in data if lib in libraries],
            key=lambda x: x[1]
        )
        
        print("\nDecoding Speed (fastest first):")
        for i, (lib, time) in enumerate(decode_ranking, 1):
            print(f"  {i}. {lib}: {time:.3f}ms")
        
        # 데이터 크기 순위
        size_ranking = sorted(
            [(lib, data[lib]["size_bytes"]) for lib in data if lib in libraries],
            key=lambda x: x[1]
        )
        
        print("\nData Size (smallest first):")
        for i, (lib, size) in enumerate(size_ranking, 1):
            print(f"  {i}. {lib}: {size:,} bytes")

async def main():
    print("Checking server at http://localhost:8080...")
    
    try:
        results = await run_benchmark()
        generate_report(results)
        
        # 결과를 JSON 파일로 저장
        with open("benchmark_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print("\nResults saved to benchmark_results.json")
        
    except httpx.ConnectError:
        print("Cannot connect to server. Please start FastAPI server first:")
        print("  uv run uvicorn app.main:app --reload --port 8080")

if __name__ == "__main__":
    asyncio.run(main())