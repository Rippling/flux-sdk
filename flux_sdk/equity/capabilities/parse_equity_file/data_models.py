from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Currency(BaseModel):
    amount: float
    currency_type: str


class EquityVestingEvent(BaseModel):
    vest_date: datetime
    vest_quantity: float
    vested_quantity: float
    vest_performance_condition: bool


class EquityGrant(BaseModel):
    external_stakeholder_identifier: str
    internal_stakeholder_identifier: str | None = None
    grant_unique_identifier: str
    grant_name: str
    grant_date: datetime
    canceled_date: datetime | None = None
    grant_price: Currency
    expiration_date: datetime | None = None
    grant_quantity: float
    exercised_quantity: float = 0.0
    released_quantity: float = 0.0
    canceled_quantity: float = 0.0
    expired_quantity: float = 0.0
    exercisable_quantity: float = 0.0
    exercise_price: Currency | None = None
    outstanding_quantity: float
    outstanding_vested_quantity: float
    outstanding_unvested_quantity: float
    vesting_events: list[EquityVestingEvent]
    extras: dict[str, Any]  # fields that are specific to some third parties and might not be needed right now
