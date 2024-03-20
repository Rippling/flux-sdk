from datetime import datetime
from decimal import Decimal
from typing import Optional

from enum import Enum

class DeductionDetails:
    companyId: str
    employeeId: str
    deductionCode: str
    effectiveFrom: datetime
    endDate: datetime
    employeeContribution: Optional[Decimal]
    companyContribution: Optional[Decimal]

class DeductionCodeField(Enum):
    EMPLOYEE_CONTRIBUTION = "EMPLOYEE_CONTRIBUTION"
    COMPANY_CONTRIBUTION = "COMPANY_CONTRIBUTION"

class ExternalDeductionCodeToRipplingCode:
    externalCode: str
    ripplingCode: str
    ripplingDeductionField: DeductionCodeField


