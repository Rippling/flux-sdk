from abc import ABC, abstractmethod

from flux_sdk.flex.capabilities.update_contributions.data_models import EmployeeContribution
from flux_sdk.flux_core.data_models import AppContext, CompanyInfo, File


class UpdateContributions(ABC):
    """Report employee payroll contributions for contribution types (FSA, HSA, etc.) in a payroll run to a benefit
     provider.

    This class represents the "update contributions" capability. The developer is supposed to implement
    get_formatted_enrollment_files in their implementation. For further details regarding their
    implementation details, check their documentation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def get_formatted_contributions_files(company_info: CompanyInfo, employee_contributions: list[EmployeeContribution],
                                          app_context: AppContext) -> list[File]:
        """A function that converts employee contributions to formatted contribution file.

        This method receives company information and a list of EmployeeContribution objects. The developer is expected
        to return the app specific list of formatted contribution files.
        :param company_info:
        :param employee_contributions:
        :param app_context:
        :return:
        """
