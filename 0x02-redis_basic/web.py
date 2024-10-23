#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import redis.typing
import requests
from functools import wraps
from typing import Awaitable, Callable, Union


def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page
    """
    @wraps(fn)
    async def wrapper(url: str) -> str:
        """ Wrapper that:
            - check whether a url's data is cached
            - tracks how many times get_page is called
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page: Union[Awaitable[bytes], bytes, None] = client.get(url)
        if cached_page is not None:
            if isinstance(cached_page, Awaitable):
                cached_page = await cached_page
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(url, response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ Makes a http request to a given endpoint
    """
    response = requests.get(url)
    return response.text
