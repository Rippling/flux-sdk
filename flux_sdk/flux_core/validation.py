from typing import Any, Type


def raise_if_missing_or_incorrect_type(obj: Any, name: str, desired_type: Type):
    value = getattr(obj, name)

    if not value:
        raise ValueError(f"{name} is required")

    raise_if_incorrect_type(obj, name, desired_type)


def raise_if_incorrect_type(obj: Any, name: str, desired_type: Type):
    value = getattr(obj, name)

    if value:
        if not isinstance(value, desired_type):
            raise TypeError(f"{name} should be a {desired_type}")