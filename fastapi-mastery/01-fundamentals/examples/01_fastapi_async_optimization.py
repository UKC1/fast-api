"""
FastAPI Async Optimization Examples
===================================

Real-world examples of optimizing FastAPI applications using async patterns.
Learn how to avoid common pitfalls and implement high-performance async code.
"""

import asyncio
import time
import random
from typing import List, Dict, Optional, AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass
import aiohttp
import aiofiles
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel


# Models
class UserCreate(BaseModel):
    name: str
    email: str
    department: str


class User(BaseModel):
    id: int
    name: str
    email: str
    department: str
    created_at: float


class APIResponse(BaseModel):
    status: str
    data: Dict
    execution_time: float


# Example 1: Database Connection Pool
class AsyncDBPool:
    """Simulated async database connection pool"""
    
    def __init__(self, max_connections: int = 10):
        self.max_connections = max_connections
        self.pool = asyncio.Queue(maxsize=max_connections)
        self.created_connections = 0
        self._lock = asyncio.Lock()
    
    async def _create_connection(self):
        """Simulate database connection creation"""
        await asyncio.sleep(0.1)  # Connection setup time
        connection_id = self.created_connections
        self.created_connections += 1
        return f"db_connection_{connection_id}"
    
    @asynccontextmanager
    async def get_connection(self):
        """Get database connection with automatic cleanup"""
        try:
            # Try to get existing connection
            connection = self.pool.get_nowait()
        except asyncio.QueueEmpty:
            # Create new connection if under limit
            async with self._lock:
                if self.created_connections < self.max_connections:
                    connection = await self._create_connection()
                else:
                    # Wait for available connection
                    connection = await self.pool.get()
        
        try:
            yield connection
        finally:
            # Return connection to pool
            await self.pool.put(connection)


# Global database pool
db_pool = AsyncDBPool(max_connections=5)


# Example 2: Optimized Data Access Layer
class UserRepository:
    """Async repository pattern for user operations"""
    
    def __init__(self, db_pool: AsyncDBPool):
        self.db_pool = db_pool
        self._users: List[User] = []  # Simulated database
        self._next_id = 1
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create user with proper async database simulation"""
        async with self.db_pool.get_connection() as conn:
            # Simulate database write operation
            await asyncio.sleep(0.05)
            
            user = User(
                id=self._next_id,
                name=user_data.name,
                email=user_data.email,
                department=user_data.department,
                created_at=time.time()
            )
            self._users.append(user)
            self._next_id += 1
            
            print(f"Created user {user.id} using {conn}")
            return user
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID with async database query"""
        async with self.db_pool.get_connection() as conn:
            # Simulate database read operation
            await asyncio.sleep(0.02)
            
            user = next((u for u in self._users if u.id == user_id), None)
            print(f"Queried user {user_id} using {conn}")
            return user
    
    async def get_users_by_department(self, department: str) -> List[User]:
        """Get users by department - optimized bulk query"""
        async with self.db_pool.get_connection() as conn:
            # Simulate complex database query
            await asyncio.sleep(0.1)
            
            users = [u for u in self._users if u.department == department]
            print(f"Queried {len(users)} users in {department} using {conn}")
            return users
    
    async def get_all_users(self) -> List[User]:
        """Get all users with pagination support"""
        async with self.db_pool.get_connection() as conn:
            await asyncio.sleep(0.03)
            
            print(f"Retrieved {len(self._users)} users using {conn}")
            return self._users.copy()


# Dependency injection
def get_user_repository() -> UserRepository:
    return UserRepository(db_pool)


# Example 3: External API Integration with Circuit Breaker
class ExternalAPIClient:
    """Async external API client with resilience patterns"""
    
    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None
        self.circuit_breaker_failures = 0
        self.circuit_breaker_threshold = 3
        self.circuit_breaker_timeout = 30
        self.circuit_breaker_opened_at = None
    
    async def get_session(self) -> aiohttp.ClientSession:
        """Lazy session creation"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=5),
                connector=aiohttp.TCPConnector(limit=10)
            )
        return self.session
    
    async def is_circuit_open(self) -> bool:
        """Check if circuit breaker is open"""
        if self.circuit_breaker_opened_at is None:
            return False
        
        if time.time() - self.circuit_breaker_opened_at > self.circuit_breaker_timeout:
            # Reset circuit breaker
            self.circuit_breaker_failures = 0
            self.circuit_breaker_opened_at = None
            return False
        
        return True
    
    async def fetch_user_profile(self, user_id: int) -> Dict:
        """Fetch external user profile with circuit breaker"""
        if await self.is_circuit_open():
            raise HTTPException(
                status_code=503, 
                detail="External service temporarily unavailable"
            )
        
        session = await self.get_session()
        
        try:
            # Simulate external API call
            url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
            async with session.get(url) as response:
                if response.status == 200:
                    # Reset failure count on success
                    self.circuit_breaker_failures = 0
                    return await response.json()
                else:
                    raise aiohttp.ClientError(f"HTTP {response.status}")
        
        except Exception as e:
            # Increment failure count
            self.circuit_breaker_failures += 1
            
            if self.circuit_breaker_failures >= self.circuit_breaker_threshold:
                self.circuit_breaker_opened_at = time.time()
                print("Circuit breaker opened due to repeated failures")
            
            raise HTTPException(
                status_code=502, 
                detail=f"External service error: {str(e)}"
            )
    
    async def close(self):
        """Cleanup session"""
        if self.session and not self.session.closed:
            await self.session.close()


# Global external API client
api_client = ExternalAPIClient()


# Example 4: Background Task Processing
class BackgroundTaskProcessor:
    """Async background task processor with queue"""
    
    def __init__(self):
        self.task_queue = asyncio.Queue()
        self.is_running = False
        self.processor_task = None
    
    async def start(self):
        """Start the background processor"""
        if not self.is_running:
            self.is_running = True
            self.processor_task = asyncio.create_task(self._process_tasks())
    
    async def stop(self):
        """Stop the background processor"""
        self.is_running = False
        if self.processor_task:
            self.processor_task.cancel()
            try:
                await self.processor_task
            except asyncio.CancelledError:
                pass
    
    async def add_task(self, task_type: str, data: Dict):
        """Add task to processing queue"""
        await self.task_queue.put({
            "type": task_type,
            "data": data,
            "created_at": time.time()
        })
    
    async def _process_tasks(self):
        """Process tasks from queue"""
        while self.is_running:
            try:
                # Wait for task with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                
                # Process different task types
                if task["type"] == "send_email":
                    await self._send_email(task["data"])
                elif task["type"] == "sync_data":
                    await self._sync_data(task["data"])
                elif task["type"] == "cleanup":
                    await self._cleanup_data(task["data"])
                
                print(f"Processed {task['type']} task")
                
            except asyncio.TimeoutError:
                # No tasks available, continue loop
                continue
            except Exception as e:
                print(f"Error processing task: {e}")
    
    async def _send_email(self, data: Dict):
        """Simulate sending email"""
        await asyncio.sleep(0.5)  # Email service delay
    
    async def _sync_data(self, data: Dict):
        """Simulate data synchronization"""
        await asyncio.sleep(1.0)  # Sync operation delay
    
    async def _cleanup_data(self, data: Dict):
        """Simulate data cleanup"""
        await asyncio.sleep(0.2)  # Cleanup delay


# Global background processor
background_processor = BackgroundTaskProcessor()


# Example 5: Streaming Responses
async def generate_user_report(department: str) -> AsyncGenerator[str, None]:
    """Generate streaming user report"""
    yield f"User Report for {department}\n"
    yield "=" * 50 + "\n"
    
    # Simulate fetching users
    await asyncio.sleep(0.1)
    users = [
        {"name": "Alice", "role": "Manager"},
        {"name": "Bob", "role": "Developer"},
        {"name": "Charlie", "role": "Designer"}
    ]
    
    for i, user in enumerate(users, 1):
        await asyncio.sleep(0.1)  # Simulate processing time
        yield f"{i}. {user['name']} - {user['role']}\n"
    
    yield "\nReport generated successfully\n"


# FastAPI Application
app = FastAPI(
    title="Async Optimization Examples",
    description="High-performance FastAPI with async patterns"
)


# Lifespan event handlers
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    print("Starting background processor...")
    await background_processor.start()
    
    yield
    
    # Shutdown
    print("Stopping background processor...")
    await background_processor.stop()
    await api_client.close()


app = FastAPI(lifespan=lifespan)


# Optimized Endpoints

@app.post("/users/", response_model=User)
async def create_user(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repository)
):
    """Create user with async database operations"""
    start_time = time.time()
    
    try:
        user = await repo.create_user(user_data)
        
        # Add background task for user setup
        await background_processor.add_task("send_email", {
            "user_id": user.id,
            "email": user.email,
            "type": "welcome"
        })
        
        return user
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{user_id}", response_model=APIResponse)
async def get_user_with_profile(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository)
):
    """Get user with external profile data - concurrent requests"""
    start_time = time.time()
    
    try:
        # Fetch user and external profile concurrently
        user_task = repo.get_user_by_id(user_id)
        profile_task = api_client.fetch_user_profile(user_id)
        
        user, profile = await asyncio.gather(
            user_task, 
            profile_task, 
            return_exceptions=True
        )
        
        if isinstance(user, Exception):
            raise HTTPException(status_code=404, detail="User not found")
        
        if isinstance(profile, Exception):
            profile = {"error": "Profile unavailable"}
        
        execution_time = time.time() - start_time
        
        return APIResponse(
            status="success",
            data={
                "user": user.dict() if user else None,
                "profile": profile
            },
            execution_time=execution_time
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/departments/{department}/users")
async def get_department_users(
    department: str,
    repo: UserRepository = Depends(get_user_repository)
):
    """Get department users with efficient batch processing"""
    start_time = time.time()
    
    try:
        users = await repo.get_users_by_department(department)
        
        # If we have many users, process in batches
        if len(users) > 10:
            # Add background task for large department sync
            await background_processor.add_task("sync_data", {
                "department": department,
                "user_count": len(users)
            })
        
        execution_time = time.time() - start_time
        
        return APIResponse(
            status="success",
            data={
                "department": department,
                "users": [user.dict() for user in users],
                "total_count": len(users)
            },
            execution_time=execution_time
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reports/users/{department}")
async def stream_user_report(department: str):
    """Stream user report for large datasets"""
    from fastapi.responses import StreamingResponse
    
    return StreamingResponse(
        generate_user_report(department),
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={department}_report.txt"}
    )


@app.get("/health")
async def health_check():
    """Health check endpoint with system status"""
    start_time = time.time()
    
    # Check various system components
    checks = {
        "database": "healthy",
        "external_api": "healthy" if not await api_client.is_circuit_open() else "degraded",
        "background_processor": "healthy" if background_processor.is_running else "unhealthy",
        "memory_usage": f"{len(db_pool._users)} users in memory"
    }
    
    execution_time = time.time() - start_time
    
    return APIResponse(
        status="healthy",
        data=checks,
        execution_time=execution_time
    )


# Performance testing endpoint
@app.get("/performance/test")
async def performance_test():
    """Test various async patterns for performance comparison"""
    results = {}
    
    # Test 1: Sequential vs Concurrent database calls
    start_time = time.time()
    repo = UserRepository(db_pool)
    
    # Sequential calls
    seq_start = time.time()
    for i in range(5):
        await repo.get_user_by_id(1)
    sequential_time = time.time() - seq_start
    
    # Concurrent calls
    conc_start = time.time()
    tasks = [repo.get_user_by_id(1) for _ in range(5)]
    await asyncio.gather(*tasks)
    concurrent_time = time.time() - conc_start
    
    results["database_calls"] = {
        "sequential_time": sequential_time,
        "concurrent_time": concurrent_time,
        "speedup": sequential_time / concurrent_time if concurrent_time > 0 else 0
    }
    
    # Test 2: Background task processing
    bg_start = time.time()
    for i in range(10):
        await background_processor.add_task("cleanup", {"item_id": i})
    results["background_tasks"] = {
        "queue_time": time.time() - bg_start,
        "tasks_queued": 10
    }
    
    total_time = time.time() - start_time
    results["total_execution_time"] = total_time
    
    return APIResponse(
        status="completed",
        data=results,
        execution_time=total_time
    )


# Run the application
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting FastAPI Async Optimization Examples")
    print("📖 Visit http://localhost:8000/docs for API documentation")
    print("⚡ Performance test: http://localhost:8000/performance/test")
    
    uvicorn.run(
        "01_fastapi_async_optimization:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )