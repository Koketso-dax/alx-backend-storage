#!/usr/bin/env python3
"""
Cache class that stores an instance of redis.Redis()
"""
import uuid
import redis
from typing import Union, Callable, Optional
from functools import wraps


class Cache:
    """ Cache class using redis store """
    def __init__(self) -> None:
        self._redis = redis.Redis()  # default: localhost:6379
        self._redis.flushdb(True)

    def count_call(method: Callable) -> Callable:
        """ Counts the number of calls for a method """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = method.__qualname__
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    def call_history(self, method: Callable) -> Callable:
        """ Stores the history of inputs & outputs of fn. """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            input_key = method.__qualname__ + ":inputs"
            output_key = method.__qualname__ + ":outputs"
            self._redis.rpush(input_key, str(args))
            output = method(self, *args, **kwargs)
            self._redis.rpush(output_key, output)
            return output
        return wrapper

    @count_call
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores value in redis and returns key """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str,
            fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """ Retrieves value from redis using key """
        value = self._redis.get(key)
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ Retrieves string value from redis using key """
        return self._redis.get(key).decode("utf-8")

    def get_int(self, key: str) -> int:
        """ Retrieves integer value from redis using key """
        return int(self._redis.get(key))

