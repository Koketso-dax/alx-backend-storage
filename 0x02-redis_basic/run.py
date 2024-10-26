#!/usr/bin/env python3
"""
Script to make a request to google.com using the cache_module
"""
import time
import redis
from web import get_page

client = redis.Redis()

if __name__ == "__main__":
    url = "https://google.com"
    count_key = f"count:{url}"
    page_key = f"page:{url}"

    # First request
    print(get_page(url))
    print(f"Call count for {url}: {client.get(count_key).decode('utf-8')}")
    print(f"Cached content for {url}: {client.get(page_key).decode('utf-8')}")

    # Wait for 10 seconds
    time.sleep(10)

    # Second request (should fetch from cache)
    
    print(f"Cached content for {url}: {client.get(page_key).decode('utf-8')}")
