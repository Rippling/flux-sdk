from abc import ABC, abstractmethod

from flux_sdk.flux_core.data_models import AppContext, CompanyInfo, File
from flux_sdk.insurance_broker.capabilities.upload_census_data.data_models import MemberData


class UploadCensusData(ABC):
    """
    This class represents the "upload census data" capability. The developer is supposed to implement
    get_formatted_census_file in their implementation. For further details regarding their
    implementation details, check their documentation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def get_formatted_census_file(company_info: CompanyInfo, member_census: list[MemberData],
                                        app_context: AppContext) -> list[File]:
        """A function that converts member census data to formatted census file.

        This method receives company information and a list of MemberData objects. The developer is expected to
        return the app specific list of formatted census files.
        :param company_info:
        :param member_census:
        :param app_context:
        :return:
        """
