"""
Exercise 1: Coroutine Basics
=============================

Learn the fundamental differences between functions and coroutines.
Understand how async/await works and practice basic async patterns.
"""

import asyncio
import time
from typing import List


# Exercise 1.1: Basic Coroutine Creation
async def greet_async(name: str, delay: float = 1.0) -> str:
    """
    TODO: Create an async function that:
    1. Waits for 'delay' seconds using await
    2. Returns a greeting message
    
    Expected behavior:
    - await greet_async("Alice", 0.5) should take ~0.5 seconds
    - Should return "Hello, Alice!"
    """
    # Your code here
    pass


# Exercise 1.2: Sequential vs Concurrent Execution
async def demonstrate_execution_difference():
    """
    TODO: Implement two approaches to calling greet_async multiple times:
    1. Sequential: Call greet_async 3 times one after another
    2. Concurrent: Call greet_async 3 times concurrently
    
    Measure and print the time difference.
    """
    names = ["Alice", "Bob", "Charlie"]
    
    # Sequential execution
    print("=== Sequential Execution ===")
    start_time = time.time()
    # Your code here for sequential calls
    sequential_time = time.time() - start_time
    print(f"Sequential time: {sequential_time:.2f} seconds")
    
    # Concurrent execution
    print("\n=== Concurrent Execution ===")
    start_time = time.time()
    # Your code here for concurrent calls
    concurrent_time = time.time() - start_time
    print(f"Concurrent time: {concurrent_time:.2f} seconds")
    
    print(f"Speedup: {sequential_time / concurrent_time:.2f}x")


# Exercise 1.3: Error Handling in Async Functions
async def fetch_data(url: str, should_fail: bool = False) -> str:
    """
    TODO: Simulate fetching data from a URL
    1. Wait for a random time between 0.5-2.0 seconds
    2. If should_fail is True, raise ValueError("Network error")
    3. Otherwise return f"Data from {url}"
    """
    # Your code here
    pass


async def handle_multiple_requests():
    """
    TODO: Make requests to multiple URLs, some of which will fail:
    1. Create a list of URLs (at least 5)
    2. Make some fail and some succeed
    3. Handle errors gracefully and collect both results and errors
    4. Print summary of successful vs failed requests
    """
    urls = [
        "https://api1.example.com",
        "https://api2.example.com", 
        "https://api3.example.com",
        "https://api4.example.com",
        "https://api5.example.com"
    ]
    
    # Your code here
    pass


# Exercise 1.4: Custom Async Context Manager
class AsyncTimer:
    """
    TODO: Implement an async context manager that:
    1. Records the start time when entering
    2. Records the end time when exiting
    3. Prints the elapsed time
    4. Supports both sync and async context manager protocols
    """
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    async def __aenter__(self):
        # Your code here
        pass
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Your code here
        pass


async def test_async_timer():
    """Test the AsyncTimer context manager"""
    async with AsyncTimer("Test operation"):
        await asyncio.sleep(1.5)
        print("Operation completed")


# Exercise 1.5: Async Generator
async def number_generator(start: int, end: int, delay: float = 0.1):
    """
    TODO: Create an async generator that:
    1. Yields numbers from start to end (inclusive)
    2. Waits for 'delay' seconds between each yield
    3. Prints each number as it's generated
    """
    # Your code here
    pass


async def consume_numbers():
    """
    TODO: Consume numbers from the async generator:
    1. Use async for loop to consume numbers from 1 to 10
    2. Process each number (e.g., calculate square)
    3. Print the processed result
    """
    # Your code here
    pass


# Exercise 1.6: Timeout Handling
async def slow_operation(duration: float) -> str:
    """Simulate a slow operation"""
    await asyncio.sleep(duration)
    return f"Operation completed after {duration} seconds"


async def test_timeouts():
    """
    TODO: Test timeout handling:
    1. Create operations with different durations (0.5s, 2s, 5s)
    2. Set a timeout of 3 seconds
    3. Handle TimeoutError appropriately
    4. Show which operations completed and which timed out
    """
    durations = [0.5, 2.0, 5.0]
    timeout = 3.0
    
    # Your code here
    pass


# Test runner
async def main():
    """Run all exercises"""
    print("🚀 Coroutine Basics Exercises\n")
    
    try:
        print("Exercise 1.1: Basic Coroutine")
        result = await greet_async("World", 0.1)
        print(f"Result: {result}\n")
        
        print("Exercise 1.2: Sequential vs Concurrent")
        await demonstrate_execution_difference()
        print()
        
        print("Exercise 1.3: Error Handling")
        await handle_multiple_requests()
        print()
        
        print("Exercise 1.4: Async Context Manager")
        await test_async_timer()
        print()
        
        print("Exercise 1.5: Async Generator")
        await consume_numbers()
        print()
        
        print("Exercise 1.6: Timeout Handling")
        await test_timeouts()
        print()
        
        print("✅ All exercises completed!")
        
    except Exception as e:
        print(f"❌ Error running exercises: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Run the exercises
    asyncio.run(main())