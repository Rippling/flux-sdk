from abc import ABC
from typing import List, Optional

from flux_sdk.user_management.data_models.base_types import User


class UserManagementInterface(ABC):
    def get_users(self) -> List[User]:
        """
        :return: list of all users present in the app.
        """
        raise NotImplementedError

    def create_user_if_not_exist(self, user: User, force_reset_password: bool = False) -> User:
        """
        :param user: the user to be created/invited
        :param bool force_reset_password: whether we force reset the password on user creation
        :return: User object if actual user get created/invited
        """
        raise NotImplementedError

    def delete_user_if_exist(self, user: User) -> Optional[bool]:
        """
        :param user: the user to be deleted/suspended
        :return: return True if deletion/suspension is successful.
        """
        raise NotImplementedError

    def get_user_by_id(self, id: str) -> Optional[User]:
        """
        user object fetched from spoke if present, None otherwise.
        :param str id: unique identifier of the user
        :rtype User: the user fetched from third party
        """
        raise NotImplementedError