from abc import ABC, abstractmethod

from flux_sdk.time_and_attendance.capabilities.job_management.data_models import GetJobAttributesResponse


class JobManagement(ABC):

    @abstractmethod
    def get_job_attributes(self) -> GetJobAttributesResponse:
        """
        A function that gets job attributes from the third-party system.

        Use this hook to fetch job attributes from the third-party system
        so that they can be matched with attributes in Rippling.
        :return: The response containing the job attributes from the third-party system.
        """

