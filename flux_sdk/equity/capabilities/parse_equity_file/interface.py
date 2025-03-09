from abc import ABC, abstractmethod
from io import StringIO

from flux_sdk.equity.capabilities.parse_equity_file.data_models import EquityGrant


class ParseEquityFile(ABC):
    """
    Parse equity data file from third party cap table providers.

    This class represents the "parse_equity_file" capability. The developer is supposed to implement
    parse_equity_file method in their implementation. For further details regarding their
    implementation details, check their documentation.
    """
    @staticmethod
    @abstractmethod
    def parse_equity_file(stream: StringIO) -> dict[str, EquityGrant]:
        """
        This method parses the equity data stream and returns a dictionary of equity grant unique identifier to equity
        grant
        """