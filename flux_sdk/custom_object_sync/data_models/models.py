from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel


class ErrorCode(Enum):
    """
    Represents error codes for domain object validation.
    This is a placeholder for the actual error codes used in validation responses.
    """

    INVALID_OBJECT_TYPE = "ERRVAL001"
    """
    Error code for invalid object type.
    """

    MISSING_MANDATORY_FIELD = "ERRVAL002"
    """
    Error code for missing mandatory field in the object payload.
    """

    INVALID_PAYLOAD = "ERRVAL003"
    """
    Error code for invalid payload structure in the object.
    """

    AUTHENTICATION_FAILED = "ERRAUT004"
    """
    Error code for authentication failure when processing the object.
    """

    CONNECTION_ERROR = "ERRCON005"
    """
    Error code for connection issues when attempting to process the object.
    """

    UNKNOWN_ERROR = "ERRUN0001"
    """
    Error code for an unknown error that occurred during object processing.
    """


class UpdatedData(BaseModel):
    """
    Represents the updates that have been made to the domain object.
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

    def __str__(self) -> str:
        return (f"UpdatedData(field_name={self.field_name}, old_value={self.old_value}, "
                f"new_value={self.new_value})")

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the updated data to a dictionary representation.
        This method is useful for serialization or logging purposes.
        """
        return {
            "field_name": self.field_name,
            "old_value": self.old_value,
            "new_value": self.new_value,
        }


class DomainObject(BaseModel):
    """
    Represents a domain object that can be received by the task.
    This is a placeholder for the actual domain object structure.
    """
    object_name: str
    """
    Object Type of the domain object, e.g., "cpq".
    """

    object_api_name: str
    """
    Object API name of the domain object, e.g., "Quotes".
    """

    payload: dict[str, Any] = {}
    """
    Payload of the domain object, containing the data related to the object.
    """

    upserted_data: list[UpdatedData] | None = None
    """
    Data that has been upserted in the object, if applicable.
    """

    last_updated_ts_utc: datetime = datetime.utcnow()
    """
    Timestamp of the domain object, indicating when it occurred.
    Timestamp is in UTC format.
    It also helpful in determining the freshness of the object.
    """

    current_change_ts_utc: datetime = datetime.utcnow()
    """
    Timestamp of the domain object, indicating when currently it was changed.
    Timestamp is in UTC format.
    """

    def __str__(self) -> str:
        return (f"DomainObject(object_name={self.object_name}, object_api_name={self.object_api_name}, "
                f"payload={self.payload}, upserted_data={self.upserted_data}, "
                f"last_updated_ts_utc={self.last_updated_ts_utc.isoformat()}, "
                f"current_change_ts_utc={self.current_change_ts_utc.isoformat()})")

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the domain object to a dictionary representation.
        This method is useful for serialization or logging purposes.
        """
        return {
            "object_name": self.object_name,
            "object_api_name": self.object_api_name,
            "payload": self.payload,
            "upserted_data": [data.to_dict() for data in self.upserted_data] if self.upserted_data else None,
            "last_updated_ts_utc": self.last_updated_ts_utc.isoformat(),
            "current_change_ts_utc": self.current_change_ts_utc.isoformat(),
        }

class ValidationResponse(BaseModel):
    """
    Represents the response from the validation of a domain object.
    This is a placeholder for the actual validation response structure.
    """
    is_valid: bool
    """
    Indicates whether the domain object is valid or not.
    """

    error_code: ErrorCode | None = None
    """
    Error code indicating the type of validation error, if any.
    """

    messages: list[str] = []
    """
    List of messages providing details about the validation status of the domain object.
    """

    def __str__(self) -> str:
        return (f"ValidationResponse(is_valid={self.is_valid}, error_code={self.error_code}, "
                f"messages={self.messages})")

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the validation response to a dictionary representation.
        This method is useful for serialization or logging purposes.
        """
        return {
            "is_valid": self.is_valid,
            "error_code": self.error_code.value if self.error_code else None,
            "messages": self.messages
        }

class PushObjectResponse(BaseModel):
    """
    Represents the response from publishing a domain object.
    This is a placeholder for the actual publish object response structure.
    """
    success: bool
    """
    Indicates whether the object was successfully published or not.
    """

    error_code: ErrorCode | None = None
    """
    Error code indicating the type of error, if any, during object publishing.
    """

    message: str | None = None
    """
    List of messages providing details about the object publishing status.
    """

    def __str__(self) -> str:
        return (f"PushObjectResponse(success={self.success}, error_code={self.error_code}, "
                f"message={self.message})")

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the push object response to a dictionary representation.
        This method is useful for serialization or logging purposes.
        """
        return {
            "success": self.success,
            "error_code": self.error_code.value if self.error_code else None,
            "message": self.message
        }


class DomainObjectRecordQuery(BaseModel):
    record_ids: list[str]
    """
    Ids of the domain object records to be queried.
    """

    query_params: dict[str, Any] | None = None
    """
    Other query parameters to filter the domain object records.
    """

    def __str__(self) -> str:
        return f"DomainObjectRecordQuery(object_ids={self.record_ids}, query_params={self.query_params})"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the domain object record query to a dictionary representation.
        This method is useful for serialization or logging purposes.
        """
        return {
            "record_ids": self.record_ids,
            "query_params": self.query_params if self.query_params else {}
        }


class DomainObjectQuery(BaseModel):
    """
    Represents a query for fetching domain objects.
    This is a placeholder for the actual query structure.
    """
    object_name: str
    """
    Object Type of the domain object, e.g., "cpq".
    """

    object_api_name: str
    """
    Object API name of the domain object, e.g., "Quotes".
    """

    record_query: DomainObjectRecordQuery
    """
    Domain object record query, which contains the object IDs and query parameters.
    """

    def __str__(self) -> str:
        return (f"DomainObjectQuery(object_name={self.object_name}, object_api_name={self.object_api_name}, "
                f"record_query={self.record_query})")

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the domain object query to a dictionary representation.
        This method is useful for serialization or logging purposes.
        """
        return {
            "object_name": self.object_name,
            "object_api_name": self.object_api_name,
            "record_query": self.record_query.to_dict()
        }


class FetchedExternalRecord(BaseModel):
    """
    Context data for the FetchDomainObjectTask.
    This class is used to pass the query parameters for fetching the domain object from the vendor.
    """
    fetched_data: dict[str, Any] = {}
    """
    Fetched data from the vendor.
    """

    fetched_by_query: DomainObjectQuery
    """
    Query parameters used to fetch the domain object.
    """

    def __str__(self) -> str:
        return f"FetchedExternalRecord(fetched_data={self.fetched_data}, fetched_by_query={self.fetched_by_query})"


class PushObjectRequest(BaseModel):
    """
    Represents the request to push a domain object to the vendor.
    This is a placeholder for the actual push request structure.
    """
    domain_object: DomainObject
    """
    The domain object to be pushed to the vendor.
    """

    request_payload: dict[str, Any]
    """
    The payload of the request to be sent to the vendor.
    This payload is typically the transformed version of the domain object.
    """

    def __str__(self) -> str:
        return f"PushObjectRequest(domain_object={self.domain_object}, request_payload={self.request_payload})"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert the push object request to a dictionary representation.
        This method is useful for serialization or logging purposes.
        """
        return {
            "domain_object": self.domain_object.to_dict(),
            "request_payload": self.request_payload
        }
