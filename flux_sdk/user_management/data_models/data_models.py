from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True)
class Organization:
    """
    This represents an organization in the third party system.
    An organization is used to group users in the third party system.
    Different third party systems may have different names of organizations:
    Github calls it "Organization", while Google Workspace calls it "Domain".
    """

    id: str
    """The unique identifier of the organization in the third party system."""

    name: Optional[str] = None
    """The name of the organization in the third party system."""


@dataclass(kw_only=True)
class User:
    """This represents a user in the third party system."""

    id: Optional[str] = None
    """The unique identifier of the user in the third party system.
     This field is required when getting users from the third party system."""

    first_name: Optional[str] = None
    """The first name of the user."""

    middle_name: Optional[str] = None
    """The middle name of the user."""

    last_name: Optional[str] = None
    """The last name of the user."""

    email: Optional[str] = None
    """The email address of the user."""


@dataclass(kw_only=True)
class GetUsersRequest:
    """This represents a request to get users from the third party system."""

    organizations: Optional[list[Organization]] = None
    """The organizations to get users from. If this field is not provided, 
    the users from all organizations should be returned."""


@dataclass(kw_only=True)
class GetUsersResponse:
    """This represents a response containing the users from the third party system."""

    users: list[User]
    """The users from the third party system."""


@dataclass(kw_only=True)
class GetOrganizationsRequest:
    """This represents a request to get organizations from the third party system."""

    pass


@dataclass(kw_only=True)
class GetOrganizationsResponse:
    """This represents a response containing the organizations from the third party system."""

    organizations: list[Organization]
    """The organizations from the third party system."""