# Python Async Programming Deep Dive

## Introduction
Understanding async programming is crucial for FastAPI mastery. This guide covers everything from basic concepts to advanced optimization techniques.

## Core Concepts

### Event Loop Fundamentals
The event loop is the heart of async programming in Python. It manages and executes async operations efficiently.

```python
import asyncio

# Basic event loop understanding
async def simple_task():
    print("Task started")
    await asyncio.sleep(1)  # Non-blocking sleep
    print("Task completed")

# Event loop controls execution
async def main():
    # Sequential execution
    await simple_task()
    await simple_task()
    
    # Concurrent execution
    await asyncio.gather(
        simple_task(),
        simple_task(),
        simple_task()
    )

# Run the event loop
asyncio.run(main())
```

### Coroutines vs Functions
Understanding the difference between regular functions and coroutines is fundamental.

```python
import time
import asyncio

# Synchronous function - blocks the thread
def sync_operation():
    time.sleep(1)  # Blocks entire thread
    return "Sync result"

# Asynchronous coroutine - yields control
async def async_operation():
    await asyncio.sleep(1)  # Yields control to event loop
    return "Async result"

# Demonstrate the difference
async def compare_operations():
    # Sync operations - total time: 3 seconds
    start = time.time()
    sync_operation()
    sync_operation()
    sync_operation()
    print(f"Sync operations took: {time.time() - start:.2f} seconds")
    
    # Async operations - total time: 1 second
    start = time.time()
    await asyncio.gather(
        async_operation(),
        async_operation(),
        async_operation()
    )
    print(f"Async operations took: {time.time() - start:.2f} seconds")
```

### Task Management
Tasks allow you to run coroutines concurrently and manage their lifecycle.

```python
import asyncio
from typing import List

async def long_running_task(task_id: int, duration: float):
    print(f"Task {task_id} started")
    try:
        await asyncio.sleep(duration)
        print(f"Task {task_id} completed")
        return f"Result from task {task_id}"
    except asyncio.CancelledError:
        print(f"Task {task_id} was cancelled")
        raise

async def task_management_demo():
    # Create tasks
    tasks: List[asyncio.Task] = []
    
    for i in range(5):
        task = asyncio.create_task(long_running_task(i, i + 1))
        tasks.append(task)
    
    # Wait for first 3 tasks to complete
    done, pending = await asyncio.wait(
        tasks, 
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # Cancel remaining tasks
    for task in pending:
        task.cancel()
    
    # Collect results
    results = []
    for task in done:
        try:
            result = await task
            results.append(result)
        except asyncio.CancelledError:
            pass
    
    return results
```

## Advanced Async Patterns

### Producer-Consumer Pattern
Essential for handling streaming data and background processing.

```python
import asyncio
import random
from asyncio import Queue
from typing import Optional

class AsyncProducerConsumer:
    def __init__(self, max_queue_size: int = 100):
        self.queue: Queue = Queue(maxsize=max_queue_size)
        self.producers_done = asyncio.Event()
    
    async def producer(self, producer_id: int, count: int):
        """Produce items and put them in the queue"""
        for i in range(count):
            # Simulate work
            await asyncio.sleep(random.uniform(0.1, 0.5))
            
            item = f"Producer-{producer_id}-Item-{i}"
            await self.queue.put(item)
            print(f"Produced: {item}")
        
        print(f"Producer {producer_id} finished")
    
    async def consumer(self, consumer_id: int):
        """Consume items from the queue"""
        while True:
            try:
                # Wait for item with timeout
                item = await asyncio.wait_for(
                    self.queue.get(), 
                    timeout=1.0
                )
                
                # Simulate processing
                await asyncio.sleep(random.uniform(0.2, 0.8))
                
                print(f"Consumer-{consumer_id} processed: {item}")
                self.queue.task_done()
                
            except asyncio.TimeoutError:
                # Check if producers are done and queue is empty
                if self.producers_done.is_set() and self.queue.empty():
                    break
                continue
    
    async def run_simulation(self):
        # Start producers
        producer_tasks = [
            asyncio.create_task(self.producer(1, 5)),
            asyncio.create_task(self.producer(2, 3)),
            asyncio.create_task(self.producer(3, 4))
        ]
        
        # Start consumers
        consumer_tasks = [
            asyncio.create_task(self.consumer(1)),
            asyncio.create_task(self.consumer(2))
        ]
        
        # Wait for all producers to finish
        await asyncio.gather(*producer_tasks)
        self.producers_done.set()
        
        # Wait for queue to be processed
        await self.queue.join()
        
        # Cancel consumers
        for task in consumer_tasks:
            task.cancel()

# Run the simulation
async def main():
    sim = AsyncProducerConsumer()
    await sim.run_simulation()

asyncio.run(main())
```

### Connection Pool Pattern
Critical for database and HTTP connections in web applications.

```python
import asyncio
import aiohttp
from typing import List, Optional
from contextlib import asynccontextmanager

class AsyncConnectionPool:
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.connections: asyncio.Queue = asyncio.Queue(maxsize=max_connections)
        self.created_connections = 0
        self._lock = asyncio.Lock()
    
    async def create_connection(self):
        """Create a new connection (simulate expensive operation)"""
        await asyncio.sleep(0.1)  # Simulate connection setup time
        return aiohttp.ClientSession()
    
    async def get_connection(self):
        """Get a connection from the pool"""
        try:
            # Try to get existing connection
            connection = self.connections.get_nowait()
            return connection
        except asyncio.QueueEmpty:
            # Create new connection if under limit
            async with self._lock:
                if self.created_connections < self.max_connections:
                    connection = await self.create_connection()
                    self.created_connections += 1
                    return connection
            
            # Wait for available connection
            return await self.connections.get()
    
    async def return_connection(self, connection):
        """Return connection to pool"""
        if not connection.closed:
            await self.connections.put(connection)
    
    @asynccontextmanager
    async def connection(self):
        """Context manager for automatic connection management"""
        conn = await self.get_connection()
        try:
            yield conn
        finally:
            await self.return_connection(conn)
    
    async def close_all(self):
        """Close all connections"""
        while not self.connections.empty():
            try:
                conn = self.connections.get_nowait()
                await conn.close()
            except asyncio.QueueEmpty:
                break

# Usage example
async def make_requests_with_pool():
    pool = AsyncConnectionPool(max_connections=3)
    
    async def fetch_url(url: str):
        async with pool.connection() as session:
            try:
                async with session.get(url) as response:
                    return await response.text()
            except Exception as e:
                return f"Error: {e}"
    
    # Make concurrent requests
    urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/delay/2", 
        "https://httpbin.org/delay/1"
    ] * 5  # 15 requests total
    
    start = asyncio.get_event_loop().time()
    results = await asyncio.gather(*[fetch_url(url) for url in urls])
    end = asyncio.get_event_loop().time()
    
    print(f"Made {len(urls)} requests in {end - start:.2f} seconds")
    print(f"Created {pool.created_connections} connections")
    
    await pool.close_all()
```

## FastAPI Specific Patterns

### Dependency Injection with Async
FastAPI's dependency injection works seamlessly with async functions.

```python
from fastapi import FastAPI, Depends
import asyncio
from typing import AsyncGenerator

app = FastAPI()

# Async dependency
async def get_database_connection():
    # Simulate database connection
    await asyncio.sleep(0.1)
    connection = {"db": "connected"}
    try:
        yield connection
    finally:
        # Cleanup
        await asyncio.sleep(0.05)
        print("Database connection closed")

# Async endpoint with async dependency
@app.get("/users/")
async def get_users(db = Depends(get_database_connection)):
    # Simulate async database query
    await asyncio.sleep(0.2)
    return {"users": ["user1", "user2"], "db_status": db}

# Background task pattern
from fastapi import BackgroundTasks

async def send_notification(email: str, message: str):
    # Simulate sending email
    await asyncio.sleep(1)
    print(f"Sent email to {email}: {message}")

@app.post("/notify/")
async def create_notification(
    email: str, 
    message: str,
    background_tasks: BackgroundTasks
):
    # Add task to background
    background_tasks.add_task(send_notification, email, message)
    return {"message": "Notification queued"}
```

## Performance Optimization

### Avoiding Common Pitfalls
Understanding what blocks the event loop is crucial.

```python
import asyncio
import time
import aiohttp
import aiofiles

# BAD: Blocking operations in async functions
async def bad_example():
    # Don't do this - blocks event loop
    time.sleep(1)  # Blocking!
    
    # Don't do this - synchronous I/O
    with open("file.txt", "r") as f:  # Blocking!
        content = f.read()
    
    return content

# GOOD: Non-blocking alternatives
async def good_example():
    # Use asyncio.sleep instead of time.sleep
    await asyncio.sleep(1)  # Non-blocking
    
    # Use async file I/O
    async with aiofiles.open("file.txt", "r") as f:  # Non-blocking
        content = await f.read()
    
    return content

# CPU-bound work should be offloaded
import concurrent.futures
import multiprocessing

def cpu_intensive_task(n: int) -> int:
    """Simulate CPU-intensive work"""
    total = 0
    for i in range(n):
        total += i ** 2
    return total

async def handle_cpu_work(n: int) -> int:
    """Handle CPU work without blocking event loop"""
    loop = asyncio.get_event_loop()
    
    # Use thread pool for CPU-bound tasks
    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = await loop.run_in_executor(
            executor, 
            cpu_intensive_task, 
            n
        )
    
    return result

# Batch operations for efficiency
async def batch_operations():
    urls = [f"https://httpbin.org/delay/{i}" for i in range(1, 6)]
    
    async with aiohttp.ClientSession() as session:
        # Process in batches to control concurrency
        batch_size = 3
        results = []
        
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            
            batch_tasks = [
                session.get(url) for url in batch
            ]
            
            batch_results = await asyncio.gather(*batch_tasks)
            results.extend(batch_results)
            
            # Optional: delay between batches
            await asyncio.sleep(0.1)
        
        return results
```

### Memory Management in Async Code
Proper resource management prevents memory leaks.

```python
import asyncio
import weakref
from typing import Dict, Set

class AsyncResourceManager:
    def __init__(self):
        self.active_tasks: Set[asyncio.Task] = set()
        self.cleanup_callbacks: Dict[int, callable] = {}
    
    def create_task(self, coro, *, name: str = None):
        """Create a task with automatic cleanup"""
        task = asyncio.create_task(coro, name=name)
        self.active_tasks.add(task)
        
        # Add cleanup callback
        task.add_done_callback(self.active_tasks.discard)
        
        return task
    
    async def cleanup_completed_tasks(self):
        """Remove references to completed tasks"""
        completed = {task for task in self.active_tasks if task.done()}
        self.active_tasks -= completed
    
    async def cancel_all_tasks(self):
        """Cancel all active tasks"""
        if self.active_tasks:
            for task in self.active_tasks:
                task.cancel()
            
            await asyncio.gather(
                *self.active_tasks, 
                return_exceptions=True
            )
            
            self.active_tasks.clear()

# Context manager for resource cleanup
class AsyncResource:
    def __init__(self, resource_id: str):
        self.resource_id = resource_id
        self.is_active = True
    
    async def __aenter__(self):
        print(f"Acquiring resource: {self.resource_id}")
        await asyncio.sleep(0.1)  # Simulate setup
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing resource: {self.resource_id}")
        self.is_active = False
        await asyncio.sleep(0.1)  # Simulate cleanup
    
    async def do_work(self):
        if not self.is_active:
            raise RuntimeError("Resource not active")
        await asyncio.sleep(0.5)
        return f"Work done with {self.resource_id}"

# Usage with proper cleanup
async def managed_resource_example():
    async with AsyncResource("db_connection") as resource:
        result = await resource.do_work()
        return result
```

## Debugging Async Code

### Common Issues and Solutions
Tools and techniques for debugging async applications.

```python
import asyncio
import logging
import traceback
from functools import wraps

# Enable asyncio debug mode
logging.basicConfig(level=logging.DEBUG)

def async_debug(func):
    """Decorator for debugging async functions"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = asyncio.get_event_loop().time()
        
        try:
            result = await func(*args, **kwargs)
            end_time = asyncio.get_event_loop().time()
            
            print(f"{func.__name__} completed in {end_time - start_time:.4f}s")
            return result
            
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            traceback.print_exc()
            raise
    
    return wrapper

@async_debug
async def potentially_problematic_function():
    await asyncio.sleep(1)
    # Simulate potential error
    if True:  # Change to False to see success path
        return "Success"
    else:
        raise ValueError("Something went wrong")

# Task monitoring
class AsyncTaskMonitor:
    def __init__(self):
        self.task_stats = {}
    
    def track_task(self, task: asyncio.Task):
        """Track task for monitoring"""
        self.task_stats[id(task)] = {
            "name": task.get_name(),
            "created": asyncio.get_event_loop().time(),
            "status": "running"
        }
        
        task.add_done_callback(self._task_completed)
    
    def _task_completed(self, task: asyncio.Task):
        """Callback when task completes"""
        task_id = id(task)
        if task_id in self.task_stats:
            self.task_stats[task_id].update({
                "completed": asyncio.get_event_loop().time(),
                "status": "completed" if not task.cancelled() else "cancelled",
                "exception": task.exception() if task.done() and not task.cancelled() else None
            })
    
    def get_stats(self):
        """Get task statistics"""
        return self.task_stats

# Usage example
async def debugging_example():
    monitor = AsyncTaskMonitor()
    
    # Create and track tasks
    task1 = asyncio.create_task(potentially_problematic_function())
    task2 = asyncio.create_task(asyncio.sleep(2))
    
    monitor.track_task(task1)
    monitor.track_task(task2)
    
    # Wait for completion
    results = await asyncio.gather(task1, task2, return_exceptions=True)
    
    # Print statistics
    stats = monitor.get_stats()
    for task_id, info in stats.items():
        duration = info.get("completed", 0) - info["created"]
        print(f"Task {info['name']}: {info['status']} in {duration:.4f}s")
        if info.get("exception"):
            print(f"  Exception: {info['exception']}")

# Run debugging example
asyncio.run(debugging_example())
```

## Best Practices Summary

1. **Always use async/await consistently**
   - Don't mix blocking operations with async code
   - Use async versions of I/O operations

2. **Manage concurrency carefully**
   - Use semaphores to limit concurrent operations
   - Batch operations to avoid overwhelming resources

3. **Handle exceptions properly**
   - Use try/except blocks in async functions
   - Consider using asyncio.gather with return_exceptions=True

4. **Monitor and debug effectively**
   - Use asyncio debug mode in development
   - Implement proper logging and monitoring

5. **Optimize for production**
   - Use connection pooling for external resources
   - Implement proper resource cleanup
   - Monitor task creation and completion

## Next Steps
- Practice with the exercises in the `exercises/` directory
- Implement the patterns in real projects
- Study FastAPI's async implementation details
- Learn about async testing strategies