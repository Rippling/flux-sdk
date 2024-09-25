from datetime import datetime
from typing import Optional


class TimeEntriesQuery:
    """
    This class unifies supported queries for time entries data. Not all apps may support
    all of these filters, it is us to app developer to determine how to handle the case
    where unsupported filters are passed in.
    """
    time_entry_ids: Optional[list[str]]
    organization_id: Optional[str]
    start_time: Optional[datetime]
    modified_time: Optional[datetime]
    end_time: Optional[datetime]

class JobShift:
    """
    This class represents the equivalent of Rippling Job Shift. It may be called different
    names in different apps, but should reflect clocked in periods. Note that these may overlap
    in time with breaks but must not overlap with other JobShifts.
    """
    id: Optional[str]
    job_title: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    description: Optional[str]

class Break:
    """
    This class represents the equivalent of Rippling TimeEntryBreak. It may be called different
    names in different apps, but should break periods. Note that these may overlap
    in time with JobShifts but must not overlap with other Breaks.
    """
    id: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    description: Optional[str]

class TimeEntry:
    """
    This class represents the equivalent of Rippling time entry object. It may be called different
    names in different apps, but should reflect the overarching record that tracks time segments of
    work and breaks as child lists.
    """
    id: str
    user_id: str
    organization_id: Optional[str]
    job_shifts: Optional[list[JobShift]]
    breaks: Optional[list[Break]]