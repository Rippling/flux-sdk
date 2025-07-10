from typing import Any

from flux_sdk.etl.data_models.domain_event import DomainEvent, PublishEventResponse, ValidationResponse


class DomainEventBridgeInterface:
    """
    Interface for the Domain Event Bridge.

    This interface defines the methods that should be implemented by any class
    that serves as a bridge for domain events.
    """

    def publish_event(self, event: DomainEvent) -> PublishEventResponse:
        """
        Publish a domain event to the vendor.
        Here app developers can implement the logic to send the event to the appropriate vendor or service.
        flux-proxy session will be used to publish the event.
        Args:
            event (dict): The domain event to be published.
        """
        raise NotImplementedError("Method 'publish_event' must be implemented.")

    def transform_event(self, event: DomainEvent) -> dict[str, Any]:
        """
        Transform a domain event before publishing it.

        Args:
            event (DomainEvent): The domain event to be transformed.

        Returns:
            dict[str, Any]: The transformed event data ready for publishing.
        """
        raise NotImplementedError("Method 'transform_event' must be implemented.")


    def validate_event(self, event: DomainEvent) -> ValidationResponse:
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
        raise NotImplementedError("Method 'validate_event' must be implemented.")
