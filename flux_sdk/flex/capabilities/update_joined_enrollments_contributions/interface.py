from abc import ABC, abstractmethod

from flux_sdk.flex.capabilities.update_joined_enrollments_contributions.data_models import (
    EmployeeJoinedEnrollmentContribution,
)
from flux_sdk.flux_core.data_models import AppContext, CompanyInfo, File


class UpdateJoinedEnrollmentsContributions(ABC):
    """
    This class represents the "update joined enrollments contributions" capability.
    The developer is supposed to implement get_formatted_enrollments_files_with_joined_contributions and
    get_formatted_contributions_files_with_joined_enrollments in their implementation.
    For further details regarding their implementation details, check their documentation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def get_formatted_enrollments_files_with_joined_contributions(
        company_info: CompanyInfo,
        employee_joined_enrollment_contributions: list[EmployeeJoinedEnrollmentContribution],
        app_context: AppContext
    ) -> list[File]:
        """A function that converts employee joined enrollment-contributions to formatted enrollments file.

        This method receives company information and a list of EmployeeJoinedEnrollmentContribution objects.
        The developer is expected to return the app specific list of formatted enrollments files.
        :param company_info:
        :param employee_joined_enrollment_contributions:
        :param app_context:
        :return:
        """

    @staticmethod
    @abstractmethod
    def get_formatted_contributions_files_with_joined_enrollments(
        company_info: CompanyInfo,
        employee_joined_enrollment_contributions: list[EmployeeJoinedEnrollmentContribution],
        app_context: AppContext
    ) -> list[File]:
        """A function that converts employee joined enrollment-contributions to formatted contributions file.

        This method receives company information and a list of EmployeeJoinedEnrollmentContribution objects.
        The developer is expected to return the app specific list of formatted contributions files.
        :param company_info:
        :param employee_joined_enrollment_contributions:
        :param app_context:
        :return:
        """
