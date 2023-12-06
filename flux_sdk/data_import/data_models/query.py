from dataclasses import dataclass
from enum import StrEnum
from typing import Any


# Each QueryType represents a particular pattern of executing queries for retrieving data.
class QueryType(StrEnum):
    # SQL indicates a database that uses text SQL queries as its primary interface, usually RDBMS but not exclusively.
    SQL = "sql"

    # MONGODB indicates a MongoDB database, which has its own query API that relies on data structures rather than text.
    MONGODB = "mongodb"


# This is returned by the "prepare_query" hook and is used by Rippling to execute the query for this app using the
# corresponding connector.
@dataclass
class Query:
    # This is always required and indicates which connector type is being used.
    type: QueryType

    # This is required for SQL connectors. It is the raw text of the query to be executed.
    sql_query: str

    # This is optional for SQL connectors. It is used to add safe interpolation of values into the query, rather than
    # requiring it to be constructed internally. In the sql_query, each "@var" will be replaced with the corresponding
    # "var" from this dict.
    sql_query_args: dict[str, Any]

    # This is required for MONGODB connectors. It indicates which collection the query will be executed in.
    mongo_collection: str

    # This is optional for MONGODB connectors. It provides the filter criteria for a basic query.
    mongo_filter: dict[str, Any]
