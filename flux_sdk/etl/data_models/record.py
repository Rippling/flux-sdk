from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional, Union

# This represents the currently supported types for Record fields. Currently, we only support these primitive types and
# do not allow for any complex/nested types.
Field = Union[str, int, float, bool, date, time, datetime, None]

# Checkpoints can be represented as either timestamp (datetime), sequence number (int) or an opaque token (str). Values
# are compared assuming an increasing sort order, so the largest value in a sync will be treated as the high-water mark
# for the next sync.
Checkpoint = Union[datetime, int, str]


# This corresponds to a row in the source database.
@dataclass
class Record:
    # The ID for this record, which becomes external_id in the Custom Object. Since only a simple, string value is
    # supported by Custom Objects, this does not need to be a full SchemaField.
    primary_key: str

    # This is the rest of the raw data for this record.
    fields: dict[str, Field]

    # This represents the links in this object. Each key is the field name, which is used to look up the target details.
    # Each value is the identifier used for the link.
    references: Optional[dict[str, str]] = None

    # This is used by the "process_records" hook to signal to Rippling the checkpoint that can be observed and recorded
    # after the sync is complete. Rippling will keep track of the *highest* value seen from all records. That value will
    # be passed to the "prepare_query" hook and can be used to adjust the query to only retrieve the records that have
    # changed since the last sync.
    #
    # This must be used to enable incremental sync, otherwise a full sync will happen each time.
    checkpoint: Optional[Checkpoint] = None

    # This flag can be used by the "process_records" hook to signal to Rippling that the object should not be imported.
    # If a Record is not found after this hook, that will be regarded as an error, so this flag should be used instead.
    drop: Optional[bool] = None
