import sys
import os
import time
import threading
import random
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import text

# Add backend to path
sys.path.append(os.getcwd())

# Set env var for config loading (using external port for host access)
# User/Pass/DB from .env.example, Port 5433 is DB_PORT_EXTERNAL
os.environ["DATABASE_URL"] = "postgresql://library_user:library_password@localhost:5433/library_db"

from backend.core.database.infrastructure.session import engine

def worker(i):
    """Worker function to simulate DB access."""
    # Simulate random variability
    time.sleep(random.uniform(0.1, 0.5))
    
    try:
        with engine.connect() as connection:
            # Hold connection for a bit to force pool usage
            result = connection.execute(text("SELECT 1"))
            val = result.scalar()
            time.sleep(0.5) 
            # print(f"Worker {i} got: {val}")
    except Exception as e:
        print(f"Worker {i} failed: {e}")

def monitor_pool():
    """Monitor pool status periodically."""
    for _ in range(5):
        time.sleep(1)
        status = engine.pool.status()
        print(f"[Pool Status] {status}")

def run_test():
    print(f"Starting Concurrency Test with Pool Size: {engine.pool.size()}")
    print("Spawning 20 concurrent workers...")
    
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_pool)
    monitor_thread.start()
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(worker, i) for i in range(20)]
        
        for future in futures:
            future.result()
            
    monitor_thread.join()
    print("Test Complete.")

if __name__ == "__main__":
    run_test()
