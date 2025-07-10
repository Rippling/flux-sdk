from abc import ABC, abstractmethod
from typing import Any

from flux_sdk.custom_object_sync.data_models.models import DomainObject, ValidationResponse


class CustomObjectInwardSync(ABC):
    """
    Interface for the Domain Event Bridge.

    This interface defines the methods that should be implemented by any class
    that serves as a bridge for domain events.
    """

    @staticmethod
    @abstractmethod
    def transform_object(object: dict[str, Any]) -> DomainObject:
        """
        Transform a domain event before publishing it.

        Args:
            object (DomainObject): The domain event to be transformed.

        Returns:
            dict[str, Any]: The transformed event data ready for publishing.
        """

    @staticmethod
    @abstractmethod
    def validate_object(object: dict[str, Any]) -> ValidationResponse:
        """
        Validate a domain event.

        Args:
            object (dict): The domain event to be validated.

        Returns:
            ValidationResponse: The response containing validation results.
            ValidationResponse is a Pydantic model that contains the validation results.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """

    @staticmethod
    @abstractmethod
    def fetch_object(query: dict[str, Any]) -> dict[str, Any]:
        """
        Fetch a domain event based on the provided query.

        Args:
            query (dict): The query parameters to filter the domain events.

        Returns:
            dict: The fetched domain event.
        """
