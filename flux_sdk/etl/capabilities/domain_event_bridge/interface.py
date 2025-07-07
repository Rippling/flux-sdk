from flux_sdk.etl.data_models.domain_event import DomainEvent, ValidationResponse


class DomainEventBridgeInterface:
    """
    Interface for the Domain Event Bridge.

    This interface defines the methods that should be implemented by any class
    that serves as a bridge for domain events.
    """

    def publish_event(self, event: DomainEvent) -> None:
        """
        Publish a domain event to the vendor.

        Args:
            event (dict): The domain event to be published.
        """
        raise NotImplementedError("Method 'publish_event' must be implemented.")

    def validate_event(self, event: DomainEvent) -> ValidationResponse:
        """
        Validate a domain event.

        Args:
            event (dict): The domain event to be validated.

        Returns:
            bool: True if the event is valid, False otherwise.
        """
        raise NotImplementedError("Method 'validate_event' must be implemented.")
