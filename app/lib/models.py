import graphene
from pydantic import BaseModel

from typing import Optional, List, Union


class RequestPOST(BaseModel):
  text: str
  topn: int = 10


class FillMaskResponseREST(BaseModel):
  text: str
  score: Union[float, None]


class FillMaskResponseGraphQL(graphene.ObjectType):
  text = graphene.String(required=True)
  score = graphene.Float()
