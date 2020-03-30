import pydantic
import typing


class Unit(pydantic.BaseModel):
    name: str
