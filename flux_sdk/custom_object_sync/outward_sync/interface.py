from abc import ABC, abstractmethod
from typing import Any

from flux_sdk.custom_object_sync.data_models.models import DomainObject, PublishObjectResponse, ValidationResponse


class CustomObjectOutwardSync(ABC):
    """
    Interface for the Domain Object Bridge.

    This interface defines the methods that should be implemented by any class
    that serves as a bridge for domain events.
    """

    @staticmethod
    @abstractmethod
    def push_object(payload: dict[str, Any]) -> PublishObjectResponse:
        """
        Publish a domain event to the vendor.
        Here app developers can implement the logic to send the event to the appropriate vendor or service.
        flux-proxy session will be used to publish the event.
        Args:
            payload (dict): The payload of domain event to be published.
        """

    @staticmethod
    @abstractmethod
    def transform_object(object: DomainObject) -> dict[str, Any]:
        """
        Transform a domain event before publishing it.

        Args:
            event (DomainObject): The domain event to be transformed.

        Returns:
            dict[str, Any]: The transformed event data ready for publishing.
        """

    @staticmethod
    @abstractmethod
    def validate_object(object: DomainObject) -> ValidationResponse:
        """
        Validate a domain event.

        Args:
            event (dict): The domain event to be validated.

        Returns:
            ValidationResponse: The response containing validation results.
            ValidationResponse is a Pydantic model that contains the validation results.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
