from abc import ABC, abstractmethod

from flux_sdk.custom_object_sync.data_models.models import (
    DomainObject,
    PushObjectRequest,
    PushObjectResponse,
    ValidationResponse,
)


class CustomObjectOutwardSync(ABC):
    """
    Interface for the Domain Object Bridge.

    This interface defines the methods that should be implemented by any class
    that serves as a bridge for domain events.
    """

    @staticmethod
    @abstractmethod
    def push_object(push_object_request: PushObjectRequest) -> PushObjectResponse:
        """
        Publish a domain event to the vendor.
        Here app developers can implement the logic to send the event to the appropriate vendor or service.
        flux-proxy session will be used to publish the event.
        Args:
            push_object_request (PushObjectRequest): The payload of domain event to be published.

        Returns:
            PushObjectResponse: The response containing the status of the push operation.
            PushObjectResponse is a Pydantic model that contains the response data.
        """

    @staticmethod
    @abstractmethod
    def transform_object(domain_object: DomainObject) -> PushObjectRequest:
        """
        Transform a domain event before publishing it.

        Args:
            domain_object (DomainObject): The domain event to be transformed.

        Returns:
            PushObjectRequest: The transformed event data ready for publishing.
        """

    @staticmethod
    @abstractmethod
    def validate_object(domain_object: DomainObject) -> ValidationResponse:
        """
        Validate a domain event.

        Args:
            domain_object (DomainObject): The domain object to be validated.

        Returns:
            ValidationResponse: The response containing validation results.
            ValidationResponse is a Pydantic model that contains the validation results.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
