from app.lib.custom_redis_connection import CustomConnection as RedisCustomConnection

import orjson
import redis

from os import environ, getenv
from typing import Callable

CACHE_TTL = 60 * 60  # in seconds

# Cache
cache = None
env_var = None
if 'REDIS_URL' in environ:
  env_var = 'REDIS_URL'
elif 'FLY_REDIS_CACHE_URL' in environ:
  env_var = 'FLY_REDIS_CACHE_URL'
if env_var:
  try:
    redis_connection_pool = redis.ConnectionPool.from_url(
      url=environ[env_var],
      db=0,
      connection_class=RedisCustomConnection
    )
    redis_connection_pool.timeout = 1.0
    redis_connection_pool.max_connections = 10
    cache = redis.Redis(
      connection_pool=redis_connection_pool,
    )
  except redis.exceptions.ConnectionError:
    pass


def get_cache(function: Callable, *args: tuple, **kwargs: dict) -> list:
  """Returns the results from the cache first if found."""
  if cache:
    cache_key = f'{getenv("CURRENT_RELEASE_ID", "")}\n{function.__name__}'
    for arg in args:
      cache_key += f'\n{arg}'
    for k, v in kwargs.items():
      cache_key += f'\n{k}={v}'
    try:
      cached_value = cache.get(cache_key)
      if cached_value:
        results = orjson.loads(cached_value.decode())
      else:  # value is not cached yet
        results = get_cache_fn_resolver(function, *args, **kwargs)
        cache.set(cache_key, orjson.dumps(results), ex=CACHE_TTL)
    except (
      redis.exceptions.ConnectionError,
      redis.exceptions.TimeoutError,
      redis.exceptions.ResponseError,
      orjson.JSONDecodeError
    ):
      results = get_cache_fn_resolver(function, *args, **kwargs)
  else:  # no cache available
    results = get_cache_fn_resolver(function, *args, **kwargs)
  return results


def get_cache_fn_resolver(function: Callable, *args: tuple, **kwargs: dict):
  if args:
    return function(*args)
  elif kwargs:
    return function(**kwargs)
  else:
    return function()
