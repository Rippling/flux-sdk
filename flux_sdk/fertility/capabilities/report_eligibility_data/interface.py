from abc import ABC, abstractmethod

from flux_sdk.fertility.capabilities.report_eligibility_data.data_models import EmployeeEligibilityRecord
from flux_sdk.flux_core.data_models import CompanyInfo, File


class ReportEligibilityData(ABC):
    """Report eligibility data for employees in your application via data in Rippling.

    This class represents the "report eligibility data" capability. The developer is supposed to implement
    format_eligibility_file in their implementation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def format_eligibility_file(
        company_info: CompanyInfo,
        employee_eligibility_records: list[EmployeeEligibilityRecord]
    ) -> File:
        """Given a list of EmployeeEligibilityRecord, prepare a file for upload to the provider.

        The file will be sent verbatim, so any compression or other formatting required by the provider
        must be applied within this function.
        :param company_info:
        :param employee_eligibility_records:
        :return:
        """
