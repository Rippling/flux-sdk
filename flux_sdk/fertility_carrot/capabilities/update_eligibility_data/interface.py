from abc import ABC, abstractmethod

from flux_sdk.flex.capabilities.update_contributions.data_models import EmployeeEligibilityRecord
from flux_sdk.flux_core.data_models import CompanyInfo, File


class UpdateEligibilityData(ABC):
    """
    This class represents the "upload eligibility data" capability. The developer is supposed to implement
    get_formatted_eligibility_data_file in their implementation. For further details regarding their
    implementation details, check their documentation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def get_formatted_eligibility_data_file(
        company_info: CompanyInfo,
        employee_eligibility_records: list[EmployeeEligibilityRecord]
    ) -> File:
        """
        Given a list of EmployeeEligibilityRecord, prepare a file for upload to the provider Carrot.
        The file will be sent SFTP, so any compression or other formatting required by the provider
        Carrot must be applied within this function.
        :param company_info:
        :param employee_eligibility_records:
        :return:
        """
