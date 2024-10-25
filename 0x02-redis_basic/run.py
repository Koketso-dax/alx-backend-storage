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
    print(f"Call count for {url}: {client.get(count_key)}")
    print(f"Cached content for {url}: {client.get(page_key)}")

    # Wait for 5 seconds
    time.sleep(5)

    # Second request (should fetch from cache)
    print(get_page(url))
    print(f"Call count for {url}: {client.get(count_key)}")
    print(f"Cached content for {url}: {client.get(page_key)}")

    # Wait for another 6 seconds (total 11 seconds)
    time.sleep(6)

    # Third request (should fetch from web again)
    print(get_page(url))
    print(f"Call count for {url}: {client.get(count_key)}")
    print(f"Cached content for {url}: {client.get(page_key)}")