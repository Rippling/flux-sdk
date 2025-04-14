from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Currency(BaseModel):
    amount: float
    currency_type: str


class EquityVestingEvent(BaseModel):
    """
    vest_date: the date on which the vesting event happens
    vest_quantity: the total quantity of the vesting event
    vested_quantity: the quantity which is vested
    vest_performance_condition: sometimes, a vesting event is tied to extra condition like employee performance,
    vest_canceled_quantity: quantity that has been canceled in the vesting event
    i.e. it's not necessarily vested past the vest_date
    """
    vest_date: datetime
    vest_quantity: float
    vested_quantity: float
    vest_performance_condition: bool
    vest_canceled_quantity: float


class EquityGrant(BaseModel):
    """
    external_stakeholder_identifier: the identifier of the equity grant owner in the third party system
    internal_stakeholder_identifier: the identifier of the equity grant owner within Rippling system, can be rwc id
    grant_unique_identifier: a unique identifier for the grant, i.e. different for each grant
    grant_name: the name of the grant
    grant_date: the date when the grant is created
    canceled_date: the date when the grant is canceled
    grant_price: the price of the grant
    expiration_date: the date when the grant is expired
    exercised_quantity: exercised quantity of the grant
    released_quantity: released quantity of the grant
    canceled_quantity: canceled quantity of the grant
    expired_quantity: expired quantity of the grant
    exercisable_quantity: exercisable quantity of the grant
    exercise_price: exercise price of the grant
    outstanding_quantity: outstanding quantity of the grant, also considered as valid quantity
    outstanding_vested_quantity: vested quantity within the outstanding quantity
    outstanding_unvested_quantity: unvested quantity within the outstanding quantity
    vesting_events: list of vesting events that belong to the grant
    extra: fields that are specific to some third parties and might not be needed in every use case
    """

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
    extras: dict[str, Any]
