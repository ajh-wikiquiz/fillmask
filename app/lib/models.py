import graphene
from pydantic import BaseModel

from typing import Optional, List, Union


class FillMaskREST(BaseModel):
  text: str
  score: Union[float, None]


class FillMaskGraphQL(graphene.ObjectType):
  text = graphene.String(required=True)
  score = graphene.Float()
