from typing import Any, Type, Union, get_args, get_origin


def check_field(obj: Any, attr: str, desired_type: Type, required: bool = False):
    value = getattr(obj, attr)

    if required and not value:
        raise ValueError(f"{attr} is required")

    if value:
        _check_type(value, attr, desired_type)


def _check_type(value: Any, attr: str, desired_type: Type):
    origin = get_origin(desired_type)
    args = get_args(desired_type)

    if origin == Union and len(args) > 0:
        if type(value) not in args:
            raise TypeError(f"{attr} should be a {desired_type}")

    elif origin == dict:
        if type(value) != origin:
            raise TypeError(f"{attr} should be a dict")

        if len(args) == 2:
            (key_type, value_type) = args

            if key_type != Any and not all(map(lambda k: isinstance(k, key_type), value.keys())):
                raise TypeError(f"{attr} should be a dict with {key_type} keys")

            if value_type != Any and not all(map(lambda k: isinstance(k, value_type), value.values())):
                raise TypeError(f"{attr} should be a dict with {value_type} values")

    elif origin == list:
        if type(value) != origin:
            raise TypeError(f"{attr} should be a list")

        if len(args) == 1:
            (value_type,) = args
            for v in value:
                _check_type(v, attr, value_type)

    elif origin == tuple:
        if type(value) != origin:
            raise TypeError(f"{attr} should be a tuple")

        for i, v in enumerate(value):
            value_type = args[i]
            if not isinstance(v, value_type):
                raise TypeError(f"{attr} should be a tuple with {value_type} as element {i}")

    elif not isinstance(value, desired_type):
        raise TypeError(f"{attr} should be a {desired_type}")
