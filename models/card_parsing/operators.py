from typing import Union, Literal

equals = '='
ge = '>='
le = '<='
not_equals = '!='

ComparisonOperator = Union[Literal[equals],
                           Literal[ge],
                           Literal[le],
                           Literal[not_equals]]

plus = '+'
minus = '-'
mult = '*'
div = '/'

NumberOperator = Union[Literal[plus],
                       Literal[minus],
                       Literal[mult],
                       Literal[div]]
Operator = Union[NumberOperator, ComparisonOperator]
