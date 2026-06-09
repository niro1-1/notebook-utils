import unittest
import time
from rate_limiter import RateLimiter, RateLimitExceeded, retry_on_rate_limit

class TestRateLimiter(unittest.TestCase):
    def test_rate_limit_exceeded(self):
        limiter = RateLimiter(max_calls=2, period=1)
        
        @limiter
        def mock_api_call():
            return "success"
        
        self.assertEqual(mock_api_call(), "success")
        self.assertEqual(mock_api_call(), "success")
        
        with self.assertRaises(RateLimitExceeded):
            mock_api_call()

    def test_retry_on_rate_limit_success(self):
        self.call_count = 0
        
        @retry_on_rate_limit(max_retries=2, delay=0.1)
        def mock_api_call():
            self.call_count += 1
            if self.call_count < 2:
                raise RateLimitExceeded("Simulated failure")
            return "success"
        
        result = mock_api_call()
        self.assertEqual(result, "success")
        self.assertEqual(self.call_count, 2)

    def test_retry_on_rate_limit_failure(self):
        self.call_count = 0
        
        @retry_on_rate_limit(max_retries=2, delay=0.1)
        def mock_api_call():
            self.call_count += 1
            raise RateLimitExceeded("Persistent failure")
        
        with self.assertRaises(RateLimitExceeded):
            mock_api_call()
        self.assertEqual(self.call_count, 3) # Initial + 2 retries

    def test_rate_limit_reset_after_period(self):
        limiter = RateLimiter(max_calls=1, period=0.1)
        
        @limiter
        def mock_api_call():
            return "success"
        
        self.assertEqual(mock_api_call(), "success")
        with self.assertRaises(RateLimitExceeded):
            mock_api_call()
        
        time.sleep(0.15)
        self.assertEqual(mock_api_call(), "success")

class TestStreamingDataLoader(unittest.TestCase):
    def test_streaming_loader_rate_limit_failure(self):
        from streaming_data_loader import StreamingDataLoader
        
        # Configure loader with 1 call max and 0 retries to force failure
        loader = StreamingDataLoader(s3_bucket='test', data_key='test', max_calls=1, period=1)
        
        # Override the retry decorator for this test to have 0 retries
        # This is a bit tricky since it's already decorated.
        # Let's instead just call it twice quickly.
        
        loader.fetch_batch() # 1st call success
        
        with self.assertRaises(RateLimitExceeded):
            loader.fetch_batch() # 2nd call fails because period=1

    def test_streaming_loader_recovery(self):
        from streaming_data_loader import StreamingDataLoader
        
        # 1 call per 0.1s, retries should help
        loader = StreamingDataLoader(s3_bucket='test', data_key='test', max_calls=1, period=0.1)
        
        # This should succeed because of retries even if called quickly
        # (Though retry delay is 0.1, 0.2, etc.)
        start_time = time.time()
        loader.fetch_batch()
        loader.fetch_batch() # Hits rate limit, retries after 0.1s
        end_time = time.time()
        
        self.assertGreaterEqual(end_time - start_time, 0.1)

if __name__ == '__main__':
    unittest.main()
