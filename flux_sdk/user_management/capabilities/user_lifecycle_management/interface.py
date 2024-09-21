from abc import ABC, abstractmethod

from flux_sdk.user_management.data_models.data_models import (
    GetOrganizationsRequest,
    GetOrganizationsResponse,
    GetUsersRequest,
    GetUsersResponse,
)


class UserLifecycleManagement(ABC):
    """
    This class represents the "user_lifecycle_management" capability.
    This capability is used to manage the lifecycle of users in the third-party system with supports including:
    - Getting user's organizations from the third-party system
    - Getting users from the third-party system
    """

    @abstractmethod
    def get_users(self, request: GetUsersRequest) -> GetUsersResponse:
        """
        A function that get users from the third-party system.

        Use this hook fetch users from the third-party system so that they can be matched with employees in Rippling.
        :param request: The request to get users from the third-party system. This request may contain the
        organizations to get users from.
        :return: The response containing the users from the third-party system.
        """


    @abstractmethod
    def get_organizations(self, request: GetOrganizationsRequest) -> GetOrganizationsResponse:
        """
        A function that get organizations from the third-party system.

        Use this hook to fetch organizations from the third-party system so that the organization information can be
        used to get users from the third-party system.
        :param request: The request to get organizations from the third-party system.
        :return: The response containing the organizations from the third-party system.
        """
