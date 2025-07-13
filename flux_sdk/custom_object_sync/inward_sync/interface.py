from abc import ABC, abstractmethod

from flux_sdk.custom_object_sync.data_models.models import (
    DomainObject,
    DomainObjectQuery,
    FetchedExternalRecord,
    ValidationResponse,
)


class CustomObjectInwardSync(ABC):
    """
    Interface for the Domain object Bridge.

    This interface defines the methods that should be implemented by any class
    that serves as a bridge for domain objects.
    """

    @staticmethod
    @abstractmethod
    def transform_object(fetched_external_record: FetchedExternalRecord) -> DomainObject:
        """
        Transform a domain object before publishing it.

        Args:
            fetched_external_record (FetchedExternalRecord): The domain object to be transformed in DomainObject format.

        Returns:
            DomainObject: The transformed object data ready for publishing.
        """

    @staticmethod
    @abstractmethod
    def validate_object(fetched_record: FetchedExternalRecord) -> ValidationResponse:
        """
        Validate a domain object.

        Args:
            fetched_record (FetchedExternalRecord): The fetched domain object to be validated.

        Returns:
            ValidationResponse: The response containing validation results.
            ValidationResponse is a Pydantic model that contains the validation results.
        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
            :param fetched_record:
        """

    @staticmethod
    @abstractmethod
    def fetch_object(query: DomainObjectQuery) -> FetchedExternalRecord:
        """
        Fetch a domain object based on the provided query.

        Args:
            query (DomainObjectQuery): The query parameters to filter the domain objects.

        Returns:
            FetchedExternalRecord: The fetched domain object.
        """
