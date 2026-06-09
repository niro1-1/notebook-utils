import time
import threading
from functools import wraps

class RateLimitExceeded(Exception):
    """Exception raised when the rate limit is exceeded."""
    pass

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with self.lock:
                now = time.time()
                # Remove calls older than the period
                self.calls = [c for c in self.calls if c > now - self.period]
                
                if len(self.calls) >= self.max_calls:
                    raise RateLimitExceeded(f"Rate limit exceeded: {self.max_calls} calls per {self.period} seconds")
                
                self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper

def retry_on_rate_limit(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except RateLimitExceeded:
                    if retries == max_retries:
                        raise
                    retries += 1
                    time.sleep(delay * (2 ** (retries - 1))) # Exponential backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator
