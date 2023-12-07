from abc import ABC, abstractmethod
from typing import Optional

from flux_sdk.etl.data_models.query import Query
from flux_sdk.etl.data_models.record import Checkpoint, Record
from flux_sdk.etl.data_models.schema import Schema


class SingleObjectImport(ABC):
    """
    This class represents the "single_object_import" capability. This is the first iteration of our Data Import
    framework, but is limited in scope to only operating on a single object at a time. This is a stepping stone towards
    a more robust system, so consider this experimental.
    """

    @staticmethod
    @abstractmethod
    def get_schema() -> Schema:
        """
        Use this hook to indicate the structure (aka: schema) for the data being imported. This is used to ensure that
        Rippling Custom Objects has a target for the extracted records to be loaded into.

        In Custom Objects, fields are not able to change their data type once they are created. As a result, new fields
        will be detected and created as expected. For existing fields, a change to a data type will result in an error,
        while other metadata changes (eg: description, enum_values) will be applied. For the time-being, migration must
        be performed by adding new fields.

        :return: Schema
        """

    @staticmethod
    @abstractmethod
    def prepare_query(schema: Schema, checkpoint: Optional[Checkpoint]) -> Query:
        """
        Use this hook to construct the query that should be run by Rippling to extract records.

        The "process_records" hook must decorate records with checkpoint in order to enable incremental sync.

        :param schema: The schema generated in the "get_schema" hook for this object.
        :param checkpoint: If included, this is an incremental sync and should adjust the Query accordingly.
        :return: Query
        """

    @staticmethod
    @abstractmethod
    def process_records(schema: Schema, records: list[Record]) -> list[Record]:
        """
        Use this hook to post-process the Records extracted via the query performed from "prepare_query". This hook is
        required in order to implement incremental sync (via checkpoint) or to dynamically drop records from the sync
        (via drop).

        If the Record does not adhere to the provided schema, such as using an incorrect/incompatible type for a field,
        the sync will fail. As such, this hook is the opportunity to massage any raw query results that may not be
        directly compatible.

        :param schema: The schema generated in the "get_schema" hook for this object.
        :param records: This batch of records should be updated
        :return: Query
        """
