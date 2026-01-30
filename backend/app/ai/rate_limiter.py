"""
Rate limiter for AI API requests.
"""

import asyncio
import time
from collections import deque
from dataclasses import dataclass
from typing import Callable


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    requests_per_minute: int = 10
    tokens_per_minute: int = 10000
    batch_size: int = 15
    min_delay_seconds: float = 0.5


class RateLimiter:
    """
    Token bucket rate limiter for API requests.
    Tracks request timestamps and enforces rate limits.
    """
    
    def __init__(self, config: RateLimitConfig | None = None):
        self.config = config or RateLimitConfig()
        self._request_times: deque[float] = deque(maxlen=100)
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """
        Wait until a request slot is available.
        Blocks if rate limit is exceeded.
        """
        async with self._lock:
            now = time.time()
            window_start = now - 60.0  # 1-minute window
            
            # Remove old timestamps
            while self._request_times and self._request_times[0] < window_start:
                self._request_times.popleft()
            
            # Check if we're at the limit
            if len(self._request_times) >= self.config.requests_per_minute:
                # Calculate wait time
                oldest = self._request_times[0]
                wait_time = oldest - window_start
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
            
            # Ensure minimum delay between requests
            if self._request_times:
                last_request = self._request_times[-1]
                time_since_last = now - last_request
                if time_since_last < self.config.min_delay_seconds:
                    await asyncio.sleep(self.config.min_delay_seconds - time_since_last)
            
            # Record this request
            self._request_times.append(time.time())
    
    def get_remaining_requests(self) -> int:
        """Get the number of remaining requests in the current window."""
        now = time.time()
        window_start = now - 60.0
        
        # Count recent requests
        recent = sum(1 for t in self._request_times if t >= window_start)
        return max(0, self.config.requests_per_minute - recent)
    
    def get_wait_time(self) -> float:
        """Get estimated wait time in seconds until next available slot."""
        if self.get_remaining_requests() > 0:
            return 0.0
        
        if not self._request_times:
            return 0.0
        
        oldest = self._request_times[0]
        now = time.time()
        window_start = now - 60.0
        
        return max(0.0, oldest - window_start)


class SyncRateLimiter:
    """Synchronous rate limiter for non-async code."""
    
    def __init__(self, config: RateLimitConfig | None = None):
        self.config = config or RateLimitConfig()
        self._request_times: deque[float] = deque(maxlen=100)
    
    def acquire(self) -> None:
        """Wait until a request slot is available."""
        now = time.time()
        window_start = now - 60.0
        
        # Remove old timestamps
        while self._request_times and self._request_times[0] < window_start:
            self._request_times.popleft()
        
        # Check if we're at the limit
        if len(self._request_times) >= self.config.requests_per_minute:
            oldest = self._request_times[0]
            wait_time = oldest - window_start
            if wait_time > 0:
                time.sleep(wait_time)
        
        # Ensure minimum delay
        if self._request_times:
            last_request = self._request_times[-1]
            time_since_last = now - last_request
            if time_since_last < self.config.min_delay_seconds:
                time.sleep(self.config.min_delay_seconds - time_since_last)
        
        self._request_times.append(time.time())
