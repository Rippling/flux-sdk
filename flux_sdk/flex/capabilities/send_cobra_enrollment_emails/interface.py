from abc import ABC, abstractmethod

from flux_sdk.flex.capabilities.send_cobra_enrollment_emails.data_models import Email
from flux_sdk.flex.capabilities.update_enrollments.data_models import EmployeeEnrollment
from flux_sdk.flux_core.data_models import AppContext, CompanyInfo


class SendCobraEnrollmentEmails(ABC):
    """
    This class represents the "send cobra enrollment emails" capability. The developer is supposed to implement
    get_emails_to_send in their implementation. For further details regarding their
    implementation details, check their documentation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def get_emails_to_send(company_info: CompanyInfo, employee_enrollments: list[EmployeeEnrollment],
                           app_context: AppContext) -> list[Email]:
        """A function that converts employee enrollments to Email objects.

        This method a list of EmployeeEnrollment objects. The developer is expected to
        return the Email objects which has to be sent to the vendor.
        :param company_info: contains information about company
        :param employee_enrollments: contains list of cobra enrollments
        :param app_context: contains information about customer_settings
        :return: List of Email objects.
        This email object generated has the fields required to send emails via rippling main.
        refer to send_email method in rippling-main/app/common/email.py
        """
