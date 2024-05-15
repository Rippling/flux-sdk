from enum import Enum
from typing import Optional

from flux_sdk.flux_core.data_models import DeductionType


class RecordTypeKeys(Enum):
    DeductionType = "D"
    LoanType = "L"


def get_deduction_type(given_ded_type: str) -> Optional[DeductionType]:
    ded_match_map = {
        "4ROTH": DeductionType.ROTH_401K,
        "4ROTC": DeductionType.ROTH_401K,
        "401K": DeductionType._401K,
        "401KC": DeductionType._401K,
        "401L": DeductionType._401K_LOAN_PAYMENT,
        "403B": DeductionType._403B,
        "401A": DeductionType.AFTER_TAX_401K,
        "401O": DeductionType._401K,
        "457B": DeductionType._457B,
        "ROTH_403B": DeductionType.ROTH_403B,
        "ROTH_457B": DeductionType.ROTH_457B,
    }
    return ded_match_map.get(given_ded_type, None)
