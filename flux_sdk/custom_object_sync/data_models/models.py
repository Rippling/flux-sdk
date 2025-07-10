from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class ErrorCode(Enum):
    """
    Represents error codes for domain event validation.
    This is a placeholder for the actual error codes used in validation responses.
    """

    INVALID_OBJECT_TYPE = "ERRVAL001"
    """
    Error code for invalid event type.
    """

    MISSING_MANDATORY_FIELD = "ERRVAL002"
    """
    Error code for missing mandatory field in the event payload.
    """

    INVALID_PAYLOAD = "ERRVAL003"
    """
    Error code for invalid payload structure in the event.
    """

    AUTHENTICATION_FAILED = "ERRAUT004"
    """
    Error code for authentication failure when processing the event.
    """

    CONNECTION_ERROR = "ERRCON005"
    """
    Error code for connection issues when attempting to process the event.
    """

    UNKNOWN_ERROR = "ERRUN0001"
    """
    Error code for an unknown error that occurred during event processing.
    """


class UpdatedData(BaseModel):
    """
    Represents the updates that have been made to the domain event.
    This is a placeholder for the actual updates structure.
    """
    field_name: str
    """
    Field name that has been updated.
    """

    old_value: str | None = None
    """
    Previous value of the field before the update.
    """

    new_value: str | None = None
    """
    New Current value of the field after the update.
    """


class DomainObject(BaseModel):
    """
    Represents a domain event that can be received by the task.
    This is a placeholder for the actual domain event structure.
    """
    object_type: str
    """
    Object Type of the domain event, e.g., "Quotes".
    """

    operation: str
    """
    Event Type of the domain event, e.g., "Create", "Update", "Delete".
    """

    payload: dict = {}
    """
    Payload of the domain event, containing the data related to the event.
    """

    upserted_data: list[UpdatedData] | None = None
    """
    Data that has been upserted in the event, if applicable.
    """

    timestamp_utc: datetime = datetime.utcnow()
    """
    Timestamp of the domain event, indicating when it occurred.
    Timestamp is in UTC format.
    It also helpful in determining the freshness of the event.
    """


class ValidationResponse(BaseModel):
    """
    Represents the response from the validation of a domain event.
    This is a placeholder for the actual validation response structure.
    """
    is_valid: bool
    """
    Indicates whether the domain event is valid or not.
    """

    error_code: ErrorCode | None = None
    """
    Error code indicating the type of validation error, if any.
    """

    messages: list[str] = []
    """
    List of messages providing details about the validation status of the domain event.
    """


class PublishObjectResponse(BaseModel):
    """
    Represents the response from publishing a domain event.
    This is a placeholder for the actual publish event response structure.
    """
    success: bool
    """
    Indicates whether the event was successfully published or not.
    """

    error_code: ErrorCode | None = None
    """
    Error code indicating the type of error, if any, during event publishing.
    """

    message: str | None = None
    """
    List of messages providing details about the event publishing status.
    """
