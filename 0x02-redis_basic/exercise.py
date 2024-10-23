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

    def replay(self, method: Callable):
        """ replays callable methods """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        inputs = self._redis.lrange(input_key, 0, -1)
        outputs = self._redis.lrange(output_key, 0, -1)
        print(f"{method.__qualname__} was called {len(inputs)} times:")
        for input, output in zip(inputs, outputs):
            print(f"{method.__qualname__}(*{input.decode('utf-8')}) ->
                  {output.decode('utf-8')}")
