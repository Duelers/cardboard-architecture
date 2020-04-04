import pydantic
import pydantic.generics
import typing
import types


class BaseModel(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid


T = typing.TypeVar('T')


# noinspection PyTypeChecker,PyTypeHints
def create_generic_model(
        model_name: str,
        *,
        __config__: typing.Type[pydantic.BaseConfig] = None,
        typevars: typing.List[typing.TypeVar],
        __module__: typing.Optional[str] = None,
        __validators__: typing.Dict[str, classmethod] = None,
        **field_definitions: typing.Any,
) -> typing.Type[pydantic.generics.GenericModel]:
    fields = {}
    annotations = {}

    for f_name, f_def in field_definitions.items():
        if isinstance(f_def, tuple):
            f_annotation, f_value = f_def
        else:
            f_annotation, f_value = None, f_def

        if f_annotation:
            annotations[f_name] = f_annotation
        fields[f_name] = f_value

    namespace = {'__annotations__': annotations}
    namespace.update(fields)

    if len(typevars) == 1:  # This is gross, but unpacking doesn't seem to work.
        generic_base = typing.Generic[typevars[0]]
    elif len(typevars) == 2:
        generic_base = typing.Generic[typevars[0], typevars[1]]
    elif len(typevars) == 3:
        generic_base = typing.Generic[typevars[0], typevars[1], typevars[2]]
    else:
        raise ValueError(f'create_generic_model takes 1-3 typevars. Got {len(typevars)}')

    return types.new_class(name=model_name, bases=(pydantic.generics.GenericModel, generic_base),
                           exec_body=lambda ns: ns.update(namespace))
