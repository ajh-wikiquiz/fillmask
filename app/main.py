from app.lib.cache import cache, get_cache
from app.lib.fillmask import fill_mask_onnx, MASK_STR
from app.lib.models import FillMaskREST, FillMaskGraphQL

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
import graphene
from starlette.graphql import GraphQLApp, GraphQLError

from typing import Dict, List

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


# Routes
@app.get('/fillmask', response_model=Dict[str, Dict[str, List[List[FillMaskREST]]]], response_class=ORJSONResponse)
@app.get('/fillmask/{text}', response_model=Dict[str, Dict[str, List[List[FillMaskREST]]]], response_class=ORJSONResponse)
async def fill_text(text: str, topn: int = 10):
  if text.count(MASK_STR) == 0:
    raise HTTPException(status_code=400, detail=f'{MASK_STR} must be present in the passed text.')
  return {'data': {'suggestions': get_cache(fill_mask_onnx, text, topn)}}


# GraphQL
class Query(graphene.ObjectType):
  suggestions = graphene.List(
    graphene.List(FillMaskGraphQL),
    text=graphene.String(required=True),
    topn=graphene.Int(default_value=10),
  )

  def resolve_suggestions(parent, info, text, topn):
    if text.count(MASK_STR) == 0:
      raise GraphQLError(message=f'{MASK_STR} must be present in the passed text.')
    return get_cache(fill_mask_onnx, text, topn)


app.add_route('/graphql', GraphQLApp(schema=graphene.Schema(query=Query)))
