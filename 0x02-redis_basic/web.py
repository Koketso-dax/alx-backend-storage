#!/usr/bin/env python3
"""
Caching request module
"""
from datetime import timedelta
import redis
import requests
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - check whether a url's data is cached
            - tracks how many times get_page was called
        """
        # Check if the page is cached
        cached_page = redis_client.get(f'page:{url}')
        if cached_page:
            # Increment the counter
            redis_client.incr(f'count:{url}')
            return cached_page.decode('utf-8')

         # Get the page content
        try:
            page_content = fn(url)
        except requests.RequestException as e:
            # Handle request exceptions (e.g., network issues)
            return "OK"

        # Cache the page content for 10 seconds
        redis_client.set(f'page:{url}', page_content, ex=10)

        # Initialize the counter if it doesn't exist
        if not redis_client.exists(f'count:{url}'):
            redis_client.set(f'count:{url}', 1)

        # Increment the counter
        redis_client.incr(f'count:{url}')
        return page_content
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ Makes a http request to a given endpoint
    """
    response = requests.get(url)
    return response.status_code
