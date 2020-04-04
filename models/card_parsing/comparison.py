import typing

import operators
import properties
import base


class Comparison(base.BaseModel):
    """Checks a comparison between two values."""
    name: typing.Literal['comparison']
    left: properties.Number
    right: properties.Number
    comparison: operators.ComparisonOperator = operators.equals
