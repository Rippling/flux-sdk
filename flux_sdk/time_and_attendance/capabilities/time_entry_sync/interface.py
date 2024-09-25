from abc import ABC, abstractmethod

from flux_sdk.time_and_attendance.capabilities.time_entry_sync.data_models import TimeEntriesQuery, TimeEntry


class TimeEntrySync(ABC):
    """Sync time entry data from 3rd party to Rippling

    This class represents the "sync time entry" capability. The developer is supposed to implement
    fetch_time_entries in their implementation.

    An instance of this class cannot be initiated unless this method is implemented.
    """

    @staticmethod
    @abstractmethod
    def fetch_time_entries(
        query: TimeEntriesQuery
    ) -> list[TimeEntry]:
        """Fetch all time entries for a given query filter.

        :param query:
        :return:
        """