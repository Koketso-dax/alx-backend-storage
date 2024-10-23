#!/usr/bin/env python3
"""
Cache class that stores an instance of redis.Redis()
"""
import uuid
import redis
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorator to count method calls """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function to count method calls """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def callhistory(method: Callable) -> Callable:
    """ Decorator to store method call history """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method):
    """ Display the history of calls of a particular function. """
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"
    num_calls = int(method.__self__._redis.get(method.__qualname__))
    print(f"{method.__qualname__} was called {num_calls} times:")
    inputs = method.__self__._redis.lrange(input_key, 0, -1)
    outputs = method.__self__._redis.lrange(output_key, 0, -1)
    for input_args, output in zip(inputs, outputs):
        print(f"{method.__qualname__}(*{input_args.decode('utf-8')
                                        }) -> {output.decode('utf-8')}")


class Cache:
    """ Cache class using redis store """
    def __init__(self) -> None:
        self._redis = redis.Redis()  # default: localhost:6379
        self._redis.flushdb(True)

    @callhistory
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores value in redis and returns key """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str,
            fn: callable = None) -> Union[str, bytes, int, float]:
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
