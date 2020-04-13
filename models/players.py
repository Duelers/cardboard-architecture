import pydantic

PlayerNumber = pydantic.conint(ge=1, le=2)
