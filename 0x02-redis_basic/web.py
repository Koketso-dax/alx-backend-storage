#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - check whether a url's data is cached
            - tracks how many times get_page is called
        """
        client = redis.Redis()
        count_key = f'count:{url}'
        page_key = url
        client.incr(count_key)
        cached_page = client.get(page_key)
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.setex(page_key, 10, response)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ Makes a http request to a given endpoint
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text
