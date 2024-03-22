from datetime import datetime
from decimal import Decimal
from enum import Enum


class DeductionDetails:
    companyId: str
    employeeId: str
    deductionCode: str
    effectiveFrom: datetime
    endDate: datetime
    employeeContribution: Decimal | None
    companyContribution: Decimal | None

class DeductionCodeField(Enum):
    EMPLOYEE_CONTRIBUTION = "EMPLOYEE_CONTRIBUTION"
    COMPANY_CONTRIBUTION = "COMPANY_CONTRIBUTION"

class ExternalDeductionCodeToRipplingCode:
    externalCode: str
    ripplingCode: str
    ripplingDeductionField: DeductionCodeField

