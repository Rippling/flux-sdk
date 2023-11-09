from datetime import date
from typing import Optional

from flux_sdk.flux_core.data_models import Employee


class EmployeeEligibilityRecord:
    employee: Employee
    dependent_first_name: Optional[str]
    dependent_last_name: Optional[str]

    # eligibility_start_date is the max of the employee start date considering plan waiting period and the plan
    # effective date
    eligibility_start_date: Optional[date]

    # If the employee is terminated, eligibility_end_date is the min of end date considering plan termination policy
    # and the plan expiration date; otherwise, it's the plan expiration date
    eligibility_end_date: Optional[date]
