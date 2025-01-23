from abc import ABC, abstractmethod

from flux_sdk.benefits_enrollments.capabilities.report_employee_enrollments.data_models import (
    ReportEmployeeEnrollmentsConfig,
)
from flux_sdk.benefits_enrollments.data_models import CompanyEnrollmentInfo
from flux_sdk.flux_core.data_models import File


class ReportEmployeeEnrollments(ABC):
    """Provides base data to formate report on empoloyee enrollments.
    
    The data on all company plans and employee enrollments will be provided.
    The app is expected to use the data to format and return a file which describes
    the data for the 3rd party.
    The returned file will be sent to the 3rd party via SFTP
    """

    @staticmethod
    @abstractmethod
    def format_employee_enrollment_data(
        config: ReportEmployeeEnrollmentsConfig,
        employee_enrollment_data: CompanyEnrollmentInfo
    ) -> File:
        """Single line short Summary of this hook's functionality.
        
        Detailed description of this hook.
        You can also include examples in markdown
        ```python
        # Some python code.
        ```
        :param param1: Short summary of what this param will do
        :param param2: Short summary of what this param will do
        :return: ReturnType
        """