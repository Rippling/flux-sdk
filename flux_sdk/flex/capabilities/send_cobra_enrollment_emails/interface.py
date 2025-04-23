from abc import ABC, abstractmethod

from flux_sdk.flex.capabilities.send_cobra_enrollment_emails.data_models import Email
from flux_sdk.flex.capabilities.update_enrollments.data_models import EmployeeEnrollment


class SendCobraEnrollmentEmails(ABC):
    """
    This class represents the "send cobra enrollment emails" capability. The developer is supposed to implement
    get_emails_to_send in their implementation. For further details regarding their
    implementation details, check their documentation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def get_emails_to_send(employee_enrollments: list[EmployeeEnrollment]) -> list[Email]:
        """A function that converts employee enrollments to Email objects.

        This method a list of EmployeeEnrollment objects. The developer is expected to
        return the Email objects which has to be sent to the vendor.
        :param employee_enrollments:
        :return: List of Email objects.
        """
