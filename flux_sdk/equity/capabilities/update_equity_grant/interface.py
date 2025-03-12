from abc import ABC, abstractmethod
from io import StringIO

from flux_sdk.equity.capabilities.update_equity_grant.data_models import EquityGrant


class UpdateEquityGrant(ABC):
    """
    Update equity grant data from third party cap table providers.

    This class represents the "update_equity_grant" capability. The developer is supposed to implement
    update_equity_grant method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """
    @staticmethod
    @abstractmethod
    def update_equity_grant(stream: StringIO) -> dict[str, EquityGrant]:
        """
        This method parses the equity data stream and returns a dictionary of equity grant unique identifier to equity
        grant
        """