from dataclasses import dataclass
from datetime import date, time, datetime
from typing import Union, Optional


# This represents the currently supported types for Record fields. Currently, we only support these primitive types and
# do not allow for any complex/nested types.
SupportedTypes = Union[str, int, float, bool, date, time, datetime, None]


# This corresponds to a row in the source database.
@dataclass
class Record:
    # The ID for this record, which becomes external_id in the Custom Object.
    primary_key: str

    # This is the rest of the raw data for this field.
    fields: dict[str, SupportedTypes]

    # This represents the links in this object, which correspond to the Schema references.
    references: list[Optional[str]]

    # This flag can be used by the "process_records" hook to signal to Rippling that the object should not be imported.
    # If a Record is not found after this hook, that will be regarded as an error, so this flag should be used instead.
    drop: bool

    # This is used by the "process_records" hook to signal to Rippling the checkpoint that can be observed and recorded
    # after the sync is complete.
    #
    # In the case of datetime/int values, Rippling will keep track of the *highest* value seen from all records. In the
    # case of str values, Rippling will only record the *last* value seen.
    #
    # In either case, this value will be passed to the "prepare_query" hook and can be used to adjust the query to only
    # retrieve the records that have changed since the last sync.
    checkpoint: Optional[Union[datetime, int, str]]
