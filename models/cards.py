import pydantic


class Card(pydantic.BaseModel):
    pass


class Castable(Card):
    cost: pydantic.conint(ge=0)


class Unit(Card):
    attack: pydantic.conint(ge=0)
    max_health: pydantic.conint(ge=0)

    current_health: int  # Can technically be negative at times.
    # Relevant when taking damage and then healing in response.


class General(Unit):
    pass


class Minion(Unit, Castable):
    pass
