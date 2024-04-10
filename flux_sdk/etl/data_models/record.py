from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Optional, Union

from flux_sdk.flux_core.validation import check_field

Field = Union[str, int, float, bool, date, time, datetime, None]
"""
This represents the currently supported types for Record fields. Currently, we only support these primitive types and do
not allow for any complex/nested types.
"""

Checkpoint = Union[datetime, int, str]
"""
Checkpoints can be represented as either timestamp (datetime), sequence number (int) or an opaque token (str). Values
are compared assuming an increasing sort order, so the largest value in a sync will be treated as the high-water mark
for the next sync.
"""


@dataclass(kw_only=True)
class Record:
    """This corresponds to a row in the source database."""

    primary_key: str
    """
    The ID for this record, which is derived from the Schema.primary_key_field and then becomes external_id in the
    Custom Object. Since only a simple, string value is supported by Custom Objects, this does not need to be a full
    SchemaField.
    """

    fields: dict[str, Field]
    """This is the rest of the raw data for this record."""

    references: Optional[dict[str, str]] = None
    """
    This represents the links in this object, which is derived from Schema.references when reading the record data from
    the source database. Each key is the field name, which is used to look up the target details. Each value is the
    identifier used for the link.

    For example, consider an Invoice object with a field named "customer_id" which is a foreign key pointing to another
    object Customer via id:
    
    ```json
    references = { "customer_id": "customer_1" }
    ```
    """

    checkpoint: Optional[Checkpoint] = None
    """
    This is populated by the "process_records" hook to signal to Rippling the checkpoint that can be observed and
    recorded after the sync is complete. Rippling will keep track of the *highest* value seen from all records. That
    value will be passed to the "prepare_query" hook and can be used to adjust the query to only retrieve the records
    that have changed since the last sync. When the checkpoint is used in the filtering, you should also sort the
    records by the checkpoint, otherwise there will likely be records missed between syncs.

    This must be used to enable incremental sync, otherwise a full sync will happen each time.
    """

    drop: Optional[bool] = None
    """
    This flag can be used by the "process_records" hook to signal to Rippling that the object should not be imported.
    If a Record is not found after this hook, that will be regarded as an error, so this flag should be used instead.
    """

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "primary_key", str, required=True)
        check_field(self, "fields", dict[str, Field], required=True)
        check_field(self, "references", dict[str, str])
        check_field(self, "checkpoint", Checkpoint)
        check_field(self, "drop", bool)
