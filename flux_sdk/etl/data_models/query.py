from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum
from typing import Any, Union, Optional


# This enum can be used to communicate a connector type to app hooks.
class Connector(Enum):
    SQL = "sql"
    MONGODB = "mongodb"


# This is the reduced list of acceptable types that can be used as SQL arguments.
SQLQueryArg = Union[str, bool, int, float, datetime, date, time]


# This is returned by the "prepare_query" hook for SQL connectors.
@dataclass
class SQLQuery:
    # This is the raw text of the query to be executed.
    text: str

    # This is used to add safe interpolation of values into the query, rather than requiring it to be constructed by the
    # hook. In the sql_query, each "@var" will be replaced with the corresponding "var" from this dict. The query text
    # must use only alphanumeric characters and underscores in variable names in order to be properly detected.
    #
    # This is where a variable like "checkpoint" could be added to have it interpolated safely and cleanly.
    args: Optional[dict[str, SQLQueryArg]] = None


# This is returned by the "prepare_query" hook for MongoDB connectors.
@dataclass
class MongoQuery:
    # This indicates which collection the query will be executed in.
    collection: str

    # This provides the filter criteria for a basic query.
    filter: Optional[dict[str, Any]] = None


# This is the list of types that can be used to represent a query.
Query = Union[SQLQuery, MongoQuery]