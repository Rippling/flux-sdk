from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from flux_sdk.flux_core.validation import check_field


@dataclass(kw_only=True)
class TimeEntriesQuery:
    """
    This class unifies supported queries for time entries data. Not all app APIs may support
    all of these filters, it is up to the app developer to handle those cases and provide the
    correct time entry list that matches the query.
    """

    start_time: datetime
    """start_time: This field denotes the time entry start datetime with timezone (after) to filter for."""

    end_time: Optional[datetime] = None
    """end_time: This field denotes the time entry end datetime with timezone (before) to filter for."""

@dataclass(kw_only=True)
class JobShift:
    """
    This class represents the equivalent of a Job Shift period. It may be called different
    names in different apps, but should reflect clocked in periods. Note that these may overlap
    in time with breaks but must not overlap with other JobShifts.
    """

    id: str
    """id: This field denotes the 3rd party job shift id."""

    job_attributes: dict[str, str]
    """job_attributes: This dict denotes the 3rd party job identifying attribute key-values that will be 
    provided with the JobShift. Non string attribute values should be serialized to strings."""

    start_time: datetime
    """start_time: This field denotes the job shift start datetime with timezone."""

    end_time: Optional[datetime] = None
    """end_time: This field denotes the job shift end datetime with timezone."""

    description: Optional[str] = None
    """description: This field denotes the 3rd party job shift description."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "job_attributes", dict[str, Any], required=True)
        check_field(self, "start_time", datetime, required=True)
        if self.start_time.tzinfo is None:
            raise ValueError("No time zone provided for start_time")
        check_field(self, "end_time", datetime)
        if self.end_time is not None and self.end_time.tzinfo is None:
            raise ValueError("No time zone provided for end_time")
        check_field(self, "description", str)

@dataclass(kw_only=True)
class Break:
    """
    This class represents the equivalent of a break duration. It may be called different
    names in different apps, but should reflect break periods. Note that these may overlap
    in time with JobShifts but must not overlap with other Breaks.
    """

    id: str
    """id: This field denotes the 3rd party break id."""

    start_time: datetime
    """start_time: This field denotes the break start datetime with timezone."""

    end_time: Optional[datetime] = None
    """end_time: This field denotes the break end datetime with timezone."""

    description: Optional[str] = None
    """description: This field denotes the 3rd party break description."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "start_time", datetime, required=True)
        if self.start_time.tzinfo is None:
            raise ValueError("No time zone provided for start_time")
        check_field(self, "end_time", datetime)
        if self.end_time is not None and self.end_time.tzinfo is None:
            raise ValueError("No time zone provided for end_time")
        check_field(self, "description", str)

@dataclass(kw_only=True)
class TimeEntry:
    """
    This class represents the equivalent of overarching time entry object. It may be called different
    names in different apps, but should reflect the overarching record that tracks time segments of
    work and breaks as child lists, but should also have its own start and end times to reflect the
    period of time the time entry covers.
    """

    id: str
    """id: This field denotes the 3rd party time entry id."""

    user_id: str
    """user_id: This field denotes the 3rd party user id this time entry belongs to."""

    job_shifts: Optional[list[JobShift]] = None
    """job_shifts: This field denotes the list of 3rd party job shifts this time entry contains."""

    breaks: Optional[list[Break]] = None
    """breaks: This field denotes the list of 3rd party breaks this time entry contains."""

    start_time: datetime
    """start_time: This field denotes the time entry start datetime with timezone."""

    end_time: Optional[datetime] = None
    """end_time: This field denotes the break end datetime with timezone."""

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "user_id", str, required=True)
        check_field(self, "job_shifts", list[JobShift])
        check_field(self, "breaks", list[Break])
        check_field(self, "start_time", datetime, required=True)
        if self.start_time.tzinfo is None:
            raise ValueError("No time zone provided for start_time")
        check_field(self, "end_time", datetime)
        if self.end_time is not None and self.end_time.tzinfo is None:
            raise ValueError("No time zone provided for end_time")
