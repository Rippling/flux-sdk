from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from flux_sdk.flux_core.validation import check_field


@dataclass(kw_only=True)
class TimeEntriesQuery:
    """
    This class unifies supported queries for time entries data. Not all apps may support
    all of these filters, it is us to app developer to determine how to handle the case
    where unsupported filters are passed in. All date time fields will contain timezone
    information.
    """
    """
    time_entry_ids: This field denotes list of 3rd party time entry ids
    """
    time_entry_ids: Optional[list[str]]
    """
    organization_id: This field denotes the 3rd party organization id
    """
    organization_id: Optional[str]
    """
    start_time: This field denotes the time entry start datetime (after) to filter for
    """
    start_time: datetime
    """
    modified_time: This field denotes the time entry modified datetime (after) to filter for
    """
    modified_time: Optional[datetime]
    """
    end_time: This field denotes the time entry end datetime (before) to filter for
    """
    end_time: Optional[datetime]

@dataclass(kw_only=True)
class JobShift:
    """
    This class represents the equivalent of Rippling Job Shift. It may be called different
    names in different apps, but should reflect clocked in periods. Note that these may overlap
    in time with breaks but must not overlap with other JobShifts. All datetime fields must
    include time zone information.
    """
    """
    id: This field denotes the 3rd party job shift id
    """
    id: str
    """
    job_title: This field denotes the 3rd party job title or job id
    """
    job: dict[str, Any]
    """
    start_time: This field denotes the job shift start datetime
    """
    start_time: datetime
    """
    end_time: This field denotes the job shift end datetime
    """
    end_time: Optional[datetime]
    """
    description: This field denotes the 3rd party job shift description
    """
    description: Optional[str]

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "job", dict[str, Any], required=True)
        check_field(self, "start_time", datetime, required=True)
        check_field(self, "end_time", datetime)
        check_field(self, "description", str)

@dataclass(kw_only=True)
class Break:
    """
    This class represents the equivalent of Rippling TimeEntryBreak. It may be called different
    names in different apps, but should reflect break periods. Note that these may overlap
    in time with JobShifts but must not overlap with other Breaks. All datetime fields must
    include time zone information.
    """
    """
    id: This field denotes the 3rd party break id
    """
    id: str
    """
    start_time: This field denotes the break start datetime
    """
    start_time: datetime
    """
    end_time: This field denotes the break end datetime
    """
    end_time: Optional[datetime]
    """
    description: This field denotes the 3rd party break description
    """
    description: Optional[str]

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "start_time", datetime, required=True)
        check_field(self, "end_time", datetime)
        check_field(self, "description", str)

@dataclass(kw_only=True)
class TimeEntry:
    """
    This class represents the equivalent of Rippling time entry object. It may be called different
    names in different apps, but should reflect the overarching record that tracks time segments of
    work and breaks as child lists. All datetime fields must include time zone information.
    """
    """
    id: This field denotes the 3rd party time entry id
    """
    id: str
    """
    user_id: This field denotes the 3rd party user id this time entry belongs to
    """
    user_id: str
    """
    organization_id: This field denotes the 3rd party organization id this time entry belongs to
    """
    organization_id: Optional[str]
    """
    job_shifts: This field denotes the list of 3rd party job shifts this time entry contains
    """
    job_shifts: Optional[list[JobShift]]
    """
    breaks: This field denotes the list of 3rd party breaks this time entry contains
    """
    breaks: Optional[list[Break]]

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "id", str, required=True)
        check_field(self, "user_id", str, required=True)
        check_field(self, "organization_id", str)
        check_field(self, "job_shifts", list[JobShift])
        check_field(self, "breaks", list[Break])
