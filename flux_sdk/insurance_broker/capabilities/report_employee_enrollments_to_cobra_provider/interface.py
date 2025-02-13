from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import AppContext, File
from flux_sdk.insurance_broker.capabilities.report_employee_enrollments_to_cobra_provider.data_models import (
    CobraEmployeeEnrollment,
)


class ReportEmployeeEnrollmentsToCobraProvider(ABC):
    """Provides base data to formate report on empoloyee enrollments.
    
    The data on all company plans and employee enrollments will be provided.
    The app is expected to use the data to format and return a file which describes
    the data for the 3rd party.
    The returned file will be sent to the 3rd party via SFTP
    """

    @staticmethod
    @abstractmethod
    def format_employee_enrollment_data(
        enrollments: list[CobraEmployeeEnrollment],
        app_context: AppContext,
    ) -> File:
        """This method is expected to use the employee data it receives to format a file to send to the 3rd party.
        
        The implementer is expected to use the employee level benefits data to format a file in the way 
        the 3rd party needs it. This will often be a CSV where each line describes a single benefit
        enrollment for an employee or a dependent.
        ```
        :param config: Includes any app config that might be helpful
        :param enrollments: Includes line level data on every employee and their dependents
        :param context: Includes any context data that might be helpful
        :return: File
        """