from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum
from typing import Any, Optional, Union

from flux_sdk.flux_core.validation import check_field


class Connector(Enum):
    """This enum can be used to communicate a connector type to app hooks."""
    SQL = "sql"
    MONGODB = "mongodb"


SQLQueryArg = Union[str, bool, int, float, datetime, date, time]
"""This is the reduced list of acceptable types that can be used as SQL arguments."""


@dataclass(kw_only=True)
class SQLQuery:
    """This is returned by the "prepare_query" hook for SQL connectors."""

    text: str
    """This is the raw text of the query to be executed."""

    args: Optional[dict[str, SQLQueryArg]] = None
    """
    This is used to add safe interpolation of values into the query, rather than requiring it to be constructed by the
    hook. In the sql_query, each "@var" will be replaced with the corresponding "var" from this dict. The query text
    must use only alphanumeric characters and underscores in variable names in order to be properly detected.

    This is where a variable like "checkpoint" could be added to have it interpolated safely and cleanly.
    """

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "text", str, required=True)
        check_field(self, "args", dict[str, SQLQueryArg])


@dataclass(kw_only=True)
class MongoQuery:
    """
    This is returned by the "prepare_query" hook for MongoDB connectors. The inclusion of filter, projection and
    aggregate support a variety of query patterns:

     - find: filter
     - find: filter + projection
     - find: projection
     - aggregate: pipeline

    By opting for none of these optional parameters, the entire collection will be retrieved.
    """

    collection: str
    """This indicates which collection the query will be executed in."""

    filter: Optional[dict[str, Any]] = None
    """
    This provides the filter criteria for a basic find operation. Most connectors will use this to filter documents by
    values or other simpler query operators.
    """

    projection: Optional[dict[str, Any]] = None
    """
    This provides the projection criteria for a basic find operation. Use this to include/exclude fields at query-time.
    """

    aggregate: Optional[list[dict[str, Any]]] = None
    """
    This allows for projection in advanced queries. Some connectors may offload more expensive operations (eg: join,
    embed) to the database through this instead of using the basic filter.
    """

    def __post_init__(self):
        """Perform validation."""
        check_field(self, "collection", str, required=True)
        check_field(self, "filter", dict[str, Any])
        check_field(self, "projection", dict[str, Any])
        check_field(self, "aggregate", list[dict[str, Any]])


Query = Union[SQLQuery, MongoQuery]
"""This is the list of types that can be used to represent a query."""
