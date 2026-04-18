"""
Exercise 1: Coroutine Basics - SOLUTION
=====================================

Complete implementation of all async programming exercises.
"""

import asyncio
import time
import random
from typing import List, Union


# Exercise 1.1: Basic Coroutine Creation
async def greet_async(name: str, delay: float = 1.0) -> str:
    """Create an async function that waits and returns a greeting"""
    await asyncio.sleep(delay)
    return f"Hello, {name}!"


# Exercise 1.2: Sequential vs Concurrent Execution
async def demonstrate_execution_difference():
    """Compare sequential vs concurrent execution performance"""
    names = ["Alice", "Bob", "Charlie"]
    
    # Sequential execution
    print("=== Sequential Execution ===")
    start_time = time.time()
    for name in names:
        result = await greet_async(name, 0.5)
        print(f"  {result}")
    sequential_time = time.time() - start_time
    print(f"Sequential time: {sequential_time:.2f} seconds")
    
    # Concurrent execution
    print("\n=== Concurrent Execution ===")
    start_time = time.time()
    tasks = [greet_async(name, 0.5) for name in names]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(f"  {result}")
    concurrent_time = time.time() - start_time
    print(f"Concurrent time: {concurrent_time:.2f} seconds")
    
    speedup = sequential_time / concurrent_time if concurrent_time > 0 else 0
    print(f"Speedup: {speedup:.2f}x")


# Exercise 1.3: Error Handling in Async Functions
async def fetch_data(url: str, should_fail: bool = False) -> str:
    """Simulate fetching data with potential failures"""
    # Random delay between 0.5-2.0 seconds
    delay = random.uniform(0.5, 2.0)
    await asyncio.sleep(delay)
    
    if should_fail:
        raise ValueError(f"Network error for {url}")
    
    return f"Data from {url}"


async def handle_multiple_requests():
    """Handle multiple requests with error management"""
    urls = [
        "https://api1.example.com",
        "https://api2.example.com", 
        "https://api3.example.com",
        "https://api4.example.com",
        "https://api5.example.com"
    ]
    
    # Make some requests fail
    should_fail_list = [False, True, False, True, False]
    
    tasks = []
    for url, should_fail in zip(urls, should_fail_list):
        task = fetch_data(url, should_fail)
        tasks.append(task)
    
    # Gather results with exception handling
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successful = 0
    failed = 0
    
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"  ❌ {urls[i]}: {result}")
            failed += 1
        else:
            print(f"  ✅ {urls[i]}: {result}")
            successful += 1
    
    print(f"\nSummary: {successful} successful, {failed} failed")


# Exercise 1.4: Custom Async Context Manager
class AsyncTimer:
    """Async context manager for timing operations"""
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
        self.end_time = None
    
    async def __aenter__(self):
        print(f"⏱️  Starting {self.name}...")
        self.start_time = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        elapsed = self.end_time - self.start_time
        
        if exc_type is not None:
            print(f"❌ {self.name} failed after {elapsed:.2f} seconds")
        else:
            print(f"✅ {self.name} completed in {elapsed:.2f} seconds")
        
        # Don't suppress exceptions
        return False


async def test_async_timer():
    """Test the AsyncTimer context manager"""
    async with AsyncTimer("Test operation"):
        await asyncio.sleep(1.5)
        print("  Operation in progress...")


# Exercise 1.5: Async Generator
async def number_generator(start: int, end: int, delay: float = 0.1):
    """Generate numbers asynchronously with delays"""
    print(f"🔢 Generating numbers from {start} to {end}")
    for number in range(start, end + 1):
        await asyncio.sleep(delay)
        print(f"  Generated: {number}")
        yield number


async def consume_numbers():
    """Consume and process numbers from async generator"""
    print("🔄 Consuming numbers and calculating squares:")
    
    async for number in number_generator(1, 5, 0.2):
        square = number ** 2
        print(f"  {number}² = {square}")


# Exercise 1.6: Timeout Handling
async def slow_operation(duration: float) -> str:
    """Simulate a slow operation"""
    await asyncio.sleep(duration)
    return f"Operation completed after {duration} seconds"


async def test_timeouts():
    """Test timeout handling with various operation durations"""
    durations = [0.5, 2.0, 5.0]
    timeout = 3.0
    
    print(f"⏰ Testing operations with {timeout}s timeout:")
    
    for duration in durations:
        try:
            print(f"  Starting {duration}s operation...")
            result = await asyncio.wait_for(
                slow_operation(duration), 
                timeout=timeout
            )
            print(f"  ✅ {result}")
            
        except asyncio.TimeoutError:
            print(f"  ⏰ Operation timed out after {timeout}s")
        
        except Exception as e:
            print(f"  ❌ Unexpected error: {e}")


# Bonus Exercise: Task Management
async def task_lifecycle_demo():
    """Demonstrate task creation, monitoring, and cancellation"""
    print("📋 Task Lifecycle Demo:")
    
    async def worker(worker_id: int, duration: float):
        try:
            print(f"  Worker {worker_id} started")
            await asyncio.sleep(duration)
            print(f"  Worker {worker_id} completed")
            return f"Result from worker {worker_id}"
        except asyncio.CancelledError:
            print(f"  Worker {worker_id} was cancelled")
            raise
    
    # Create multiple tasks
    tasks = [
        asyncio.create_task(worker(1, 1.0)),
        asyncio.create_task(worker(2, 2.0)),
        asyncio.create_task(worker(3, 3.0)),
    ]
    
    # Wait for first task to complete
    done, pending = await asyncio.wait(
        tasks, 
        return_when=asyncio.FIRST_COMPLETED
    )
    
    print(f"  First task completed, cancelling remaining {len(pending)} tasks")
    
    # Cancel remaining tasks
    for task in pending:
        task.cancel()
    
    # Wait for all tasks to finish (including cancelled ones)
    final_results = await asyncio.gather(*tasks, return_exceptions=True)
    
    print("  Final results:")
    for i, result in enumerate(final_results, 1):
        if isinstance(result, asyncio.CancelledError):
            print(f"    Task {i}: Cancelled")
        elif isinstance(result, Exception):
            print(f"    Task {i}: Error - {result}")
        else:
            print(f"    Task {i}: {result}")


# Test runner
async def main():
    """Run all exercises with timing"""
    print("🚀 Coroutine Basics Exercises - SOLUTIONS\n")
    
    exercises = [
        ("Basic Coroutine", test_basic_coroutine),
        ("Sequential vs Concurrent", demonstrate_execution_difference),
        ("Error Handling", handle_multiple_requests),
        ("Async Context Manager", test_async_timer),
        ("Async Generator", consume_numbers),
        ("Timeout Handling", test_timeouts),
        ("Task Lifecycle", task_lifecycle_demo),
    ]
    
    total_start = time.time()
    
    for name, exercise_func in exercises:
        print(f"{'='*50}")
        print(f"Exercise: {name}")
        print(f"{'='*50}")
        
        try:
            if name == "Basic Coroutine":
                result = await greet_async("World", 0.1)
                print(f"Result: {result}")
            else:
                await exercise_func()
            
            print(f"✅ {name} completed successfully\n")
            
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    total_time = time.time() - total_start
    print(f"🎉 All exercises completed in {total_time:.2f} seconds!")


async def test_basic_coroutine():
    """Wrapper for basic coroutine test"""
    result = await greet_async("World", 0.1)
    print(f"Result: {result}")


if __name__ == "__main__":
    # Enable debug mode for learning
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the exercises
    asyncio.run(main(), debug=True)