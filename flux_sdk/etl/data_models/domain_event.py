from pydantic import BaseModel


class UpdatedData(BaseModel):
    """
    Represents the updates that have been made to the domain event.
    This is a placeholder for the actual updates structure.
    """
    field_name: str
    old_value: str | None = None
    new_value: str | None = None


class DomainEvent(BaseModel):
    """
    Represents a domain event that can be received by the task.
    This is a placeholder for the actual domain event structure.
    """
    object_type: str
    event_type: str
    payload: dict
    upserted_data: list[UpdatedData] | None = None
    timestamp: str


class ValidationResponse(BaseModel):
    """
    Represents the response from the validation of a domain event.
    This is a placeholder for the actual validation response structure.
    """
    is_valid: bool
    error_messages: list[str] | None = None
