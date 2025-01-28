from datetime import date
from typing import Optional

class Leave:
    def __init__(self, leave_management_services_indicator: Optional[str] = None):
        self.leave_management_services_indicator = self.validate_indicator(leave_management_services_indicator)

    @staticmethod
    def validate_indicator(value: Optional[str]) -> Optional[str]:
        if value is not None and value not in ["Y", "N"]:
            raise ValueError("Leave Management Services Indicator must be 'Y' or 'N'.")
        return value
