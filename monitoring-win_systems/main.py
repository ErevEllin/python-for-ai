import psutil
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def monitor_application(pid, interval=5):
    """Monitor a Python process and log its resource usage."""
    process = psutil.Process(pid)

    while True:
        try:
            # Get CPU and memory usage
            cpu_percent = process.cpu_percent(interval=0.1)
            memory_info = process.memory_info()

            logger.info(f"PID {pid} - CPU: {cpu_percent}% - Memory: {memory_info.rss / 1024 / 1024:.2f} MB")

            time.sleep(interval)
        except psutil.NoSuchProcess:
            logger.error(f"Process {pid} no longer exists")
            break
        except Exception as e:
            logger.error(f"Monitoring error: {e}")
            break

# Example usage: monitor_application(your_app_pid, interval=5)
monitor_application(4476, interval=5)  # Replace 12345 with the actual PID of the Python process you want to monitor
