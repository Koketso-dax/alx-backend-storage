#!/usr/bin/env python3
"""
Cache class that stores an instance of redis.Redis()
"""
from typing import Union
import uuid
import redis


class Cache:
    """ Cache class using redis store """
    def __init__(self) -> None:
        self._redis = redis.Redis() # default: localhost:6379
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores value in redis and returns key """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key
