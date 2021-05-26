from app.lib.custom_redis_connection import CustomConnection as RedisCustomConnection
from app.lib.fillmask import fill_mask_onnx, MASK_STR
from app.lib.models import Request, FillMaskREST, FillMaskGraphQL

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
import orjson
import redis
from starlette.graphql import GraphQLApp, GraphQLError

from os import environ
from typing import Dict, List

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
      url=environ.get(env_var),
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

# Initialization
app = FastAPI()

# Allow CORS
app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['*'],
)


def fill_mask_onnx_cache(text: str) -> list:
  """Returns the most similar results from the cache first if found.
  """
  if cache:
    try:
      cached_value = cache.get(text)
      if cached_value:
        results = orjson.loads(cached_value.decode())
      else:  # value is not cached yet
        results = fill_mask_onnx(text)
        cache.set(text, orjson.dumps(results))
    except (
      redis.exceptions.ConnectionError,
      redis.exceptions.TimeoutError,
      redis.exceptions.ResponseError,
      orjson.JSONDecodeError
    ):
      results = fill_mask_onnx(text)
  else:  # no cache available
    results = fill_mask_onnx(text)
  return results


# Routes
@app.get('/fillmask', response_model=Dict[str, Dict[str, List[List[FillMaskREST]]]], response_class=ORJSONResponse)
@app.get('/fillmask/{text}', response_model=Dict[str, Dict[str, List[List[FillMaskREST]]]], response_class=ORJSONResponse)
async def fill_text(text: str):
  if text.count(MASK_STR) == 0:
    raise HTTPException(status_code=400, detail=f'{MASK_STR} must be present in the passed text.')
  return {'data': {'suggestions': fill_mask_onnx_cache(text)}}


# GraphQL
class Query(graphene.ObjectType):
  fill_mask = graphene.List(graphene.List(FillMaskGraphQL), text=graphene.String(required=True))

  def resolve_fill_mask(parent, info, text):
    if text.count(MASK_STR) == 0:
      raise GraphQLError(message=f'{MASK_STR} must be present in the passed text.')
    return fill_mask_onnx_cache(text)


app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))
