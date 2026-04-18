"""
Exercise 2: Event Loop Control
==============================

Master event loop management, task scheduling, and advanced async patterns.
Learn how to control async execution flow effectively.
"""

import asyncio
import time
import random
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running" 
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskInfo:
    """Information about a running task"""
    name: str
    created_at: float
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None


# Exercise 2.1: Custom Task Manager
class AsyncTaskManager:
    """
    TODO: Implement a task manager that can:
    1. Create and track tasks with names
    2. Monitor task status and completion
    3. Cancel specific tasks or all tasks
    4. Provide statistics about task execution
    5. Handle task dependencies
    """
    
    def __init__(self):
        self.tasks: Dict[str, asyncio.Task] = {}
        self.task_info: Dict[str, TaskInfo] = {}
        self.completed_tasks: List[str] = []
    
    async def create_task(self, coro, name: str) -> str:
        """
        TODO: Create and track a new task
        - Generate unique task ID if name exists
        - Store task info and start monitoring
        - Return task ID
        """
        # Your code here
        pass
    
    async def wait_for_task(self, task_name: str, timeout: Optional[float] = None):
        """
        TODO: Wait for a specific task to complete
        - Handle timeout if specified
        - Return task result or raise exception
        """
        # Your code here
        pass
    
    async def cancel_task(self, task_name: str) -> bool:
        """
        TODO: Cancel a specific task
        - Return True if cancelled, False if not found or already done
        """
        # Your code here
        pass
    
    async def cancel_all_tasks(self):
        """
        TODO: Cancel all running tasks
        """
        # Your code here
        pass
    
    def get_task_stats(self) -> Dict[str, Any]:
        """
        TODO: Return statistics about tasks
        - Total created, running, completed, failed, cancelled
        - Average execution time
        - Current memory usage (task count)
        """
        # Your code here
        pass


# Exercise 2.2: Priority Task Scheduler
class PriorityTaskScheduler:
    """
    TODO: Implement a priority-based task scheduler that:
    1. Accepts tasks with priority levels (1=highest, 10=lowest)
    2. Executes higher priority tasks first
    3. Supports task dependencies
    4. Limits concurrent execution
    """
    
    def __init__(self, max_concurrent_tasks: int = 3):
        self.max_concurrent = max_concurrent_tasks
        self.pending_tasks: List = []  # Priority queue
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)
    
    async def schedule_task(self, coro, priority: int = 5, 
                          dependencies: List[str] = None) -> str:
        """
        TODO: Schedule a task with priority
        - Store in priority queue
        - Check dependencies
        - Start execution if possible
        """
        # Your code here
        pass
    
    async def _execute_next_task(self):
        """
        TODO: Execute the next highest priority task
        - Check dependencies are satisfied
        - Respect concurrency limits
        """
        # Your code here
        pass
    
    async def wait_for_all(self):
        """
        TODO: Wait for all tasks to complete
        """
        # Your code here
        pass


# Exercise 2.3: Async Resource Pool
class AsyncResourcePool:
    """
    TODO: Implement a generic async resource pool that:
    1. Manages a pool of reusable resources (e.g., connections)
    2. Provides async context manager for resource acquisition
    3. Handles resource health checking
    4. Supports pool resizing
    """
    
    def __init__(self, resource_factory: Callable, 
                 max_size: int = 10, min_size: int = 2):
        self.resource_factory = resource_factory
        self.max_size = max_size
        self.min_size = min_size
        self.pool: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self.created_resources = 0
        self._lock = asyncio.Lock()
    
    async def _create_resource(self):
        """
        TODO: Create a new resource using the factory
        """
        # Your code here
        pass
    
    async def acquire(self):
        """
        TODO: Acquire a resource from the pool
        - Create new if pool is empty and under max_size
        - Wait for available resource otherwise
        """
        # Your code here
        pass
    
    async def release(self, resource):
        """
        TODO: Return resource to pool
        - Validate resource health
        - Put back in pool or discard if unhealthy
        """
        # Your code here
        pass
    
    async def resource(self):
        """
        TODO: Context manager for automatic resource management
        """
        # Your code here - implement async context manager
        pass


# Exercise 2.4: Event-Driven System
class AsyncEventBus:
    """
    TODO: Implement an async event bus that:
    1. Allows components to publish and subscribe to events
    2. Supports async event handlers
    3. Handles event handler errors gracefully
    4. Supports event filtering and middleware
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.middleware: List[Callable] = []
    
    def subscribe(self, event_type: str, handler: Callable):
        """
        TODO: Subscribe to an event type
        """
        # Your code here
        pass
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """
        TODO: Unsubscribe from an event type
        """
        # Your code here
        pass
    
    async def publish(self, event_type: str, data: Any):
        """
        TODO: Publish an event to all subscribers
        - Apply middleware
        - Handle errors in individual handlers
        - Don't let one handler failure affect others
        """
        # Your code here
        pass
    
    def add_middleware(self, middleware_func: Callable):
        """
        TODO: Add middleware that processes all events
        """
        # Your code here
        pass


# Exercise 2.5: Async Rate Limiter
class AsyncRateLimiter:
    """
    TODO: Implement a rate limiter that:
    1. Limits operations per time window
    2. Supports burst capacity
    3. Uses token bucket or sliding window algorithm
    4. Provides async context manager interface
    """
    
    def __init__(self, max_requests: int, time_window: float):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests: List[float] = []
        self._lock = asyncio.Lock()
    
    async def acquire(self):
        """
        TODO: Acquire permission to proceed
        - Check if request is within limits
        - Wait if necessary
        """
        # Your code here
        pass
    
    async def __aenter__(self):
        """TODO: Context manager entry"""
        # Your code here
        pass
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """TODO: Context manager exit"""
        # Your code here
        pass


# Test functions for exercises
async def test_task_manager():
    """Test the AsyncTaskManager"""
    print("Testing AsyncTaskManager...")
    
    async def sample_work(duration: float, should_fail: bool = False):
        await asyncio.sleep(duration)
        if should_fail:
            raise ValueError("Task failed!")
        return f"Work completed in {duration}s"
    
    manager = AsyncTaskManager()
    
    # TODO: Test creating, monitoring, and cancelling tasks
    # Your test code here
    pass


async def test_priority_scheduler():
    """Test the PriorityTaskScheduler"""
    print("Testing PriorityTaskScheduler...")
    
    async def priority_work(name: str, duration: float, priority: int):
        print(f"Starting {name} (priority {priority})")
        await asyncio.sleep(duration)
        print(f"Completed {name}")
        return f"{name} done"
    
    scheduler = PriorityTaskScheduler(max_concurrent_tasks=2)
    
    # TODO: Test priority-based execution
    # Your test code here
    pass


async def test_resource_pool():
    """Test the AsyncResourcePool"""
    print("Testing AsyncResourcePool...")
    
    class MockConnection:
        def __init__(self, conn_id: int):
            self.id = conn_id
            self.is_healthy = True
        
        def __str__(self):
            return f"Connection-{self.id}"
    
    async def connection_factory():
        # Simulate connection creation time
        await asyncio.sleep(0.1)
        return MockConnection(random.randint(1000, 9999))
    
    pool = AsyncResourcePool(connection_factory, max_size=3)
    
    # TODO: Test resource acquisition and release
    # Your test code here
    pass


async def test_event_bus():
    """Test the AsyncEventBus"""
    print("Testing AsyncEventBus...")
    
    event_bus = AsyncEventBus()
    
    async def user_handler(data):
        print(f"User handler received: {data}")
        await asyncio.sleep(0.1)
    
    async def audit_handler(data):
        print(f"Audit handler received: {data}")
        await asyncio.sleep(0.05)
    
    # TODO: Test event publishing and subscription
    # Your test code here
    pass


async def test_rate_limiter():
    """Test the AsyncRateLimiter"""
    print("Testing AsyncRateLimiter...")
    
    # Create limiter: 3 requests per 2 seconds
    limiter = AsyncRateLimiter(max_requests=3, time_window=2.0)
    
    async def rate_limited_operation(op_id: int):
        async with limiter:
            print(f"Operation {op_id} executing at {time.time():.2f}")
            await asyncio.sleep(0.1)
            return f"Operation {op_id} completed"
    
    # TODO: Test rate limiting behavior
    # Your test code here
    pass


# Main test runner
async def main():
    """Run all exercises"""
    print("🔄 Event Loop Control Exercises\n")
    
    exercises = [
        ("Task Manager", test_task_manager),
        ("Priority Scheduler", test_priority_scheduler),
        ("Resource Pool", test_resource_pool),
        ("Event Bus", test_event_bus),
        ("Rate Limiter", test_rate_limiter),
    ]
    
    for name, test_func in exercises:
        print(f"{'='*50}")
        print(f"Exercise: {name}")
        print(f"{'='*50}")
        
        try:
            await test_func()
            print(f"✅ {name} test completed\n")
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()
            print()
    
    print("🎉 All event loop exercises completed!")


if __name__ == "__main__":
    asyncio.run(main())