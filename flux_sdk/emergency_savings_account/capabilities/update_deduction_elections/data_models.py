from datetime import datetime
from typing import Optional

from flux_sdk.flux_core.data_models import DeductionType


class EmployeeDeductionSetting(object):
    """
    This is the return type for "parse_deductions" method in the UpdateDeductionElections
    interface.
    """
    ssn: str
    client_id: Optional[str]  # The client identifier to be sent if available.
    effective_date: datetime
    deduction_type: DeductionType
    value: float
    is_percentage: bool
    id: str
