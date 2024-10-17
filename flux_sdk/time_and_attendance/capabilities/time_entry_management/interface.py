from abc import ABC, abstractmethod

from flux_sdk.time_and_attendance.capabilities.time_entry_management.data_models import (
    GetBreakTypesResponse,
    TimeEntriesQuery,
    TimeEntry,
)


class TimeEntryManagement(ABC):
    """Sync time entry related data from 3rd party to Rippling

    This class represents the TimeEntryManagement capability. The developer is supposed to implement
    fetch_time_entries and fetch_break_types in their implementation.

    An instance of this class cannot be initiated unless both methods are implemented.
    """

    @abstractmethod
    def fetch_time_entries(
        self,
        query: TimeEntriesQuery
    ) -> list[TimeEntry]:
        """Fetch all time entries for a given query filter.

        :param query: The query filter to fetch time entries.
        :return: A list of time entries that match the query.
        """

    @abstractmethod
    def get_break_types(self) -> GetBreakTypesResponse:
        """
        A function that gets the break types defined in the third party system.

        Use this hook to fetch the break types so that the customer can map them to the break types in Rippling.

        When importing the type entries, the breaks should contain the break type id, which can be resolved to the
        break type in Rippling.

        :return: The response containing all the break types available in the third party system.
        """
