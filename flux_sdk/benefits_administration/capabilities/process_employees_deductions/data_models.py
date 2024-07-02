from datetime import datetime
from decimal import Decimal
from enum import Enum


class DeductionDetails:
    company_id: str
    employee_id: str
    deduction_code: str
    effective_from: datetime
    end_date: datetime | None
    employee_contribution: Decimal | None
    company_contribution: Decimal | None
    imputed_income: Decimal | None

class DeductionCodeField(Enum):
    EMPLOYEE_CONTRIBUTION = "EMPLOYEE_CONTRIBUTION"
    COMPANY_CONTRIBUTION = "COMPANY_CONTRIBUTION"
    IMPUTED_INCOME = "IMPUTED_INCOME"

class ExternalDeductionCodeToRipplingCode:
    external_code: str
    rippling_code: str
    rippling_deduction_field: DeductionCodeField

