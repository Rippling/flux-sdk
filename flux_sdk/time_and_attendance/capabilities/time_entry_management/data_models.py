from datetime import datetime
from typing import Optional


class TimeEntriesQuery:
    """
    This class unifies supported queries for time entries data. Not all apps may support
    all of these filters, it is us to app developer to determine how to handle the case
    where unsupported filters are passed in.
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
    start_time: Optional[datetime]
    """
    modified_time: This field denotes the time entry modified datetime (after) to filter for
    """
    modified_time: Optional[datetime]
    """
    end_time: This field denotes the time entry end datetime (before) to filter for
    """
    end_time: Optional[datetime]

class JobShift:
    """
    This class represents the equivalent of Rippling Job Shift. It may be called different
    names in different apps, but should reflect clocked in periods. Note that these may overlap
    in time with breaks but must not overlap with other JobShifts.
    """
    """
    id: This field denotes the 3rd party job shift id
    """
    id: Optional[str]
    """
    job_title: This field denotes the 3rd party job title or job id
    """
    job_title: str
    """
    start_time: This field denotes the job shift start datetime
    """
    start_time: Optional[datetime]
    """
    end_time: This field denotes the job shift end datetime
    """
    end_time: Optional[datetime]
    """
    description: This field denotes the 3rd party job shift description
    """
    description: Optional[str]

class Break:
    """
    This class represents the equivalent of Rippling TimeEntryBreak. It may be called different
    names in different apps, but should reflect break periods. Note that these may overlap
    in time with JobShifts but must not overlap with other Breaks.
    """
    """
    id: This field denotes the 3rd party break id
    """
    id: Optional[str]
    """
    start_time: This field denotes the break start datetime
    """
    start_time: Optional[datetime]
    """
    end_time: This field denotes the break end datetime
    """
    end_time: Optional[datetime]
    """
    description: This field denotes the 3rd party break description
    """
    description: Optional[str]

class TimeEntry:
    """
    This class represents the equivalent of Rippling time entry object. It may be called different
    names in different apps, but should reflect the overarching record that tracks time segments of
    work and breaks as child lists.
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