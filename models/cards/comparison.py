import typing

from . import operators
from . import properties
from . import base


class Comparison(base.BaseModel):
    """Checks a comparison between two values."""
    name: typing.Literal['comparison']
    left: properties.Number
    right: properties.Number
    comparison: operators.ComparisonOperator = operators.equals
