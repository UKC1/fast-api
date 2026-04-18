import asyncio
import time
import statistics
from typing import List, Dict
import httpx
import json

BASE_URL = "http://localhost:8080"

async def test_endpoint(client: httpx.AsyncClient, url: str, iterations: int = 10) -> Dict:
    times = []
    
    for _ in range(iterations):
        start = time.perf_counter()
        response = await client.get(url)
        elapsed = (time.perf_counter() - start) * 1000
        times.append(elapsed)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} for {url}")
            return None
    
    return {
        "avg_ms": round(statistics.mean(times), 3),
        "min_ms": round(min(times), 3),
        "max_ms": round(max(times), 3),
        "median_ms": round(statistics.median(times), 3),
        "stdev_ms": round(statistics.stdev(times), 3) if len(times) > 1 else 0
    }

async def run_performance_tests():
    async with httpx.AsyncClient(timeout=30.0) as client:
        test_cases = [10, 100, 1000, 5000]
        
        print("\n" + "="*80)
        print("JSON LIBRARY PERFORMANCE COMPARISON")
        print("="*80)
        
        for count in test_cases:
            print(f"\n>> Testing with {count} records:")
            print("-" * 60)
            
            # Test each library
            results = {}
            
            # Standard JSON
            url = f"{BASE_URL}/json/standard/{count}"
            print(f"Testing standard JSON...")
            perf = await test_endpoint(client, url, iterations=5)
            if perf:
                results["json"] = perf
            
            # orjson
            url = f"{BASE_URL}/json/orjson/{count}"
            print(f"Testing orjson...")
            perf = await test_endpoint(client, url, iterations=5)
            if perf:
                results["orjson"] = perf
            
            # ujson
            url = f"{BASE_URL}/json/ujson/{count}"
            print(f"Testing ujson...")
            perf = await test_endpoint(client, url, iterations=5)
            if perf:
                results["ujson"] = perf
            
            # Compare all
            print(f"\n>> Direct comparison endpoint test...")
            url = f"{BASE_URL}/json/compare/{count}"
            response = await client.get(url)
            if response.status_code == 200:
                comparison_data = response.json()
                
                print(f"\n>> Results for {count} records:")
                print(f"{'Library':<10} {'Encode(ms)':<12} {'Decode(ms)':<12} {'Total(ms)':<12} {'API Avg(ms)':<12}")
                print("-" * 70)
                
                for lib in ["json", "orjson", "ujson"]:
                    if lib in comparison_data["comparison"] and lib in results:
                        comp = comparison_data["comparison"][lib]
                        api = results[lib]
                        print(f"{lib:<10} {comp['encode_ms']:<12.3f} {comp['decode_ms']:<12.3f} {comp['total_ms']:<12.3f} {api['avg_ms']:<12.3f}")
                
                print(f"\n>> Winners:")
                print(f"  Fastest Encoder: {comparison_data['fastest_encoder']}")
                print(f"  Fastest Decoder: {comparison_data['fastest_decoder']}")
                print(f"  Fastest Overall: {comparison_data['fastest_overall']}")

async def load_test():
    print("\n" + "="*80)
    print("LOAD TEST - 100 concurrent requests with 1000 records")
    print("="*80)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        for lib in ["standard", "orjson", "ujson"]:
            url = f"{BASE_URL}/json/{lib}/1000"
            
            print(f"\n>> Load testing {lib}...")
            
            start = time.perf_counter()
            tasks = [client.get(url) for _ in range(100)]
            responses = await asyncio.gather(*tasks)
            total_time = (time.perf_counter() - start) * 1000
            
            success_count = sum(1 for r in responses if r.status_code == 200)
            
            print(f"  Total time: {total_time:.3f}ms")
            print(f"  Successful: {success_count}/100")
            print(f"  Avg per request: {total_time/100:.3f}ms")

if __name__ == "__main__":
    print("Starting JSON Performance Tests...")
    print("Make sure the FastAPI server is running on http://localhost:8080")
    
    try:
        asyncio.run(run_performance_tests())
        asyncio.run(load_test())
        print("\n>> All tests completed!")
    except httpx.ConnectError:
        print("\n>> Error: Could not connect to the server.")
        print("Please make sure the FastAPI server is running:")
        print("  uvicorn app.main:app --reload --port 8080")
    except Exception as e:
        print(f"\n>> Error: {e}")