import pydantic
import typing


class BaseAnimation(pydantic.BaseModel):
    def animate(self):
        pass


class MoveAnimation(BaseAnimation):
    pass
