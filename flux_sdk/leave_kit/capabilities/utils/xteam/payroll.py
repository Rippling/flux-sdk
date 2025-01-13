from datetime import date
from typing import Optional

class Payroll:
    def __init__(
        self,
        scheduled_hours_per_week: int,
        last_12_months_hours: int,
        cumulative_hours_end_date: Optional[date] = None,
        cumulative_hours_number_of_weeks: Optional[int] = None
    ):
        self.scheduled_hours_per_week = self.validate_hours(scheduled_hours_per_week, "Scheduled Hours Per Week")
        self.last_12_months_hours = self.validate_hours(last_12_months_hours, "Last 12 Months Hours", is_cumulative=True)
        self.cumulative_hours_end_date = cumulative_hours_end_date
        self.cumulative_hours_number_of_weeks = self.validate_weeks(cumulative_hours_number_of_weeks)

    @staticmethod
    def validate_hours(hours: int, field_name: str, is_cumulative: bool = False) -> int:
        if hours < 0:
            raise ValueError(f"{field_name} cannot be negative.")
        if is_cumulative and hours > 999999:
            raise ValueError(f"{field_name} must be a 6-digit number with an implied decimal.")
        return hours

    @staticmethod
    def validate_weeks(weeks: Optional[int]) -> Optional[int]:
        if weeks is not None:
            if not (0 <= weeks <= 99):
                raise ValueError("Cumulative Hours Number of Weeks must be between 0 and 99.")
        return weeks
