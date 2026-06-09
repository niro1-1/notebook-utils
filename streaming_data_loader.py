import time
from rate_limiter import RateLimiter, retry_on_rate_limit, RateLimitExceeded

class StreamingDataLoader:
    """
    A data loader that simulates streaming data from S3 with rate limiting.
    """
    def __init__(self, s3_bucket, data_key, batch_size=10, max_calls=5, period=1):
        self.s3_bucket = s3_bucket
        self.data_key = data_key
        self.batch_size = batch_size
        self.limiter = RateLimiter(max_calls=max_calls, period=period)
        self.total_batches = 20
        self.current_batch = 0

    @retry_on_rate_limit(max_retries=3, delay=0.1)
    def fetch_batch(self):
        # Simulate a call that might be rate limited
        return self._fetch_from_s3()

    def _fetch_from_s3(self):
        # This is where the actual rate limiting is applied via the decorator/limiter
        # In a real app, this would be a boto3 call.
        # Here we manually use the limiter to simulate the failure.
        
        @self.limiter
        def _execute():
            self.current_batch += 1
            return [f"data_{self.current_batch}_{i}" for i in range(self.batch_size)]
        
        return _execute()

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_batch >= self.total_batches:
            raise StopIteration
        return self.fetch_batch()
