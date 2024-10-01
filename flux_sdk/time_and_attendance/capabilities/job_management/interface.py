from abc import ABC, abstractmethod

from flux_sdk.time_and_attendance.capabilities.job_management.data_models import (
    GetJobAttributesResponse,
    GetJobAttributeValuesRequest,
    GetJobAttributeValuesResponse,
)


class JobManagement(ABC):

    @abstractmethod
    def get_job_attributes(self) -> GetJobAttributesResponse:
        """
        A function that gets job attributes from the third-party system.

        Use this hook to fetch job attributes from the third-party system
        so that they can be matched with attributes in Rippling.
        :return: The response containing the job attributes from the third-party system.
        """

    @abstractmethod
    def get_job_attribute_values(self, request: GetJobAttributeValuesRequest) -> GetJobAttributeValuesResponse:
        """
        A function that gets job attributes mapped to their values from the third-party system.

        Use this hook to fetch job attributes mapped to their values from the third-party system.

        The values should be formatted to match a Rippling .*CompatibleValue dataclass.
        :return: The response which is a map of third party attributes to their values.
        """

