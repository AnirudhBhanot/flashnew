"""
Background task processing for long-running operations
"""
import asyncio
import logging
import uuid
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from enum import Enum
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import queue

logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskResult:
    """Result of a background task"""
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.created_at = datetime.utcnow()
        self.started_at = None
        self.completed_at = None
        self.progress = 0
        self.message = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "status": self.status.value,
            "result": self.result,
            "error": str(self.error) if self.error else None,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress": self.progress,
            "message": self.message,
            "duration_seconds": (
                (self.completed_at - self.started_at).total_seconds()
                if self.completed_at and self.started_at
                else None
            )
        }


class BackgroundTaskManager:
    """Manage background tasks"""
    
    def __init__(self, max_workers: int = 4):
        self.tasks: Dict[str, TaskResult] = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue = queue.Queue()
        self._shutdown = False
        
        # Start task processor thread
        self.processor_thread = threading.Thread(target=self._process_tasks, daemon=True)
        self.processor_thread.start()
    
    def _process_tasks(self):
        """Process tasks from the queue"""
        while not self._shutdown:
            try:
                # Get task from queue with timeout
                task_data = self.task_queue.get(timeout=1)
                if task_data is None:
                    break
                
                task_id, func, args, kwargs = task_data
                self._execute_task(task_id, func, args, kwargs)
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Error processing task: {e}")
    
    def _execute_task(self, task_id: str, func: Callable, args: tuple, kwargs: dict):
        """Execute a task in the thread pool"""
        task_result = self.tasks.get(task_id)
        if not task_result:
            return
        
        try:
            # Update status
            task_result.status = TaskStatus.RUNNING
            task_result.started_at = datetime.utcnow()
            
            # Execute the function
            if asyncio.iscoroutinefunction(func):
                # Handle async functions
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(func(*args, **kwargs))
                finally:
                    loop.close()
            else:
                # Handle sync functions
                result = func(*args, **kwargs)
            
            # Update result
            task_result.status = TaskStatus.COMPLETED
            task_result.result = result
            task_result.completed_at = datetime.utcnow()
            task_result.progress = 100
            
        except Exception as e:
            logger.error(f"Task {task_id} failed: {e}")
            task_result.status = TaskStatus.FAILED
            task_result.error = e
            task_result.completed_at = datetime.utcnow()
    
    def submit_task(
        self,
        func: Callable,
        *args,
        task_id: Optional[str] = None,
        **kwargs
    ) -> str:
        """Submit a task for background execution"""
        task_id = task_id or str(uuid.uuid4())
        
        # Create task result
        task_result = TaskResult(task_id)
        self.tasks[task_id] = task_result
        
        # Add to queue
        self.task_queue.put((task_id, func, args, kwargs))
        
        logger.info(f"Submitted task {task_id}")
        return task_id
    
    def get_task_status(self, task_id: str) -> Optional[TaskResult]:
        """Get the status of a task"""
        return self.tasks.get(task_id)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        task_result = self.tasks.get(task_id)
        if task_result and task_result.status == TaskStatus.PENDING:
            task_result.status = TaskStatus.CANCELLED
            task_result.completed_at = datetime.utcnow()
            return True
        return False
    
    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all tasks and their status"""
        return {
            task_id: task_result.to_dict()
            for task_id, task_result in self.tasks.items()
        }
    
    def cleanup_completed_tasks(self, older_than_seconds: int = 3600):
        """Remove completed tasks older than specified time"""
        now = datetime.utcnow()
        to_remove = []
        
        for task_id, task_result in self.tasks.items():
            if task_result.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                if task_result.completed_at:
                    age = (now - task_result.completed_at).total_seconds()
                    if age > older_than_seconds:
                        to_remove.append(task_id)
        
        for task_id in to_remove:
            del self.tasks[task_id]
        
        logger.info(f"Cleaned up {len(to_remove)} old tasks")
        return len(to_remove)
    
    def shutdown(self):
        """Shutdown the task manager"""
        self._shutdown = True
        self.task_queue.put(None)  # Signal processor to stop
        self.executor.shutdown(wait=True)


# Global task manager instance
task_manager = BackgroundTaskManager()


# Async task examples for FLASH

async def async_batch_predict(startup_batch: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Process multiple startup predictions in batch"""
    from models.unified_orchestrator_v3_integrated import UnifiedOrchestratorV3
    from type_converter_simple import TypeConverter
    
    orchestrator = UnifiedOrchestratorV3()
    type_converter = TypeConverter()
    
    results = []
    for i, startup_data in enumerate(startup_batch):
        try:
            # Simulate progress updates
            progress = (i / len(startup_batch)) * 100
            logger.info(f"Batch prediction progress: {progress:.1f}%")
            
            # Convert and predict
            features = type_converter.convert_frontend_to_backend(startup_data)
            result = orchestrator.predict(features)
            results.append({
                "startup_name": startup_data.get("startup_name", f"Startup {i+1}"),
                "prediction": result
            })
            
        except Exception as e:
            results.append({
                "startup_name": startup_data.get("startup_name", f"Startup {i+1}"),
                "error": str(e)
            })
    
    return {
        "total": len(startup_batch),
        "successful": len([r for r in results if "prediction" in r]),
        "failed": len([r for r in results if "error" in r]),
        "results": results
    }


async def async_generate_report(
    startup_id: str,
    include_patterns: bool = True,
    include_comparisons: bool = True
) -> Dict[str, Any]:
    """Generate comprehensive startup report"""
    import time
    
    # Simulate long-running report generation
    report = {
        "startup_id": startup_id,
        "generated_at": datetime.utcnow().isoformat(),
        "sections": []
    }
    
    # Section 1: Basic Analysis
    await asyncio.sleep(1)  # Simulate processing
    report["sections"].append({
        "name": "Basic Analysis",
        "status": "completed"
    })
    
    # Section 2: Pattern Analysis
    if include_patterns:
        await asyncio.sleep(2)  # Simulate processing
        report["sections"].append({
            "name": "Pattern Analysis",
            "status": "completed",
            "patterns_found": ["EFFICIENT_B2B_SAAS", "PLG_EFFICIENT"]
        })
    
    # Section 3: Peer Comparisons
    if include_comparisons:
        await asyncio.sleep(1.5)  # Simulate processing
        report["sections"].append({
            "name": "Peer Comparisons",
            "status": "completed",
            "peers_analyzed": 10
        })
    
    return report


# Function to run sync functions in background
def run_in_background(func: Callable, *args, **kwargs) -> str:
    """Helper to run any function in background"""
    return task_manager.submit_task(func, *args, **kwargs)