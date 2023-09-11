import abc
from abc import abstractmethod

from flux_sdk.flex.capabilities.update_enrollments.data_models import EmployeeEnrollment
from flux_sdk.flux_core.data_models import AppContext, CompanyInfo, File


class UpdateEnrollments(metaclass=abc.ABCMeta):
    """
    This class represents the "update enrollments" capability. The developer is supposed to implement
    get_formatted_enrollment_files in their implementation. For further details regarding their
    implementation details, check their documentation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "get_formatted_enrollment_files") and callable(subclass.get_formatted_enrollment_files)
            or NotImplemented
        )

    @staticmethod
    @abstractmethod
    def get_formatted_enrollments_files(company_info: CompanyInfo, employee_enrollments: list[EmployeeEnrollment],  app_context: AppContext) -> list[File]:
        """
        This method receives company information and a list of EmployeeEnrollment objects. The developer is expected to
        return the app specific list of formatted enrollment files.
        :param company_info:
        :param employee_enrollments:
        :return:
        """
