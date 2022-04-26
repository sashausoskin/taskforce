from entities.organization import Organization
from entities.user import User
from repositories.org_repository import org_repository
from services.user_service import user_service


class InvalidCode(Exception):
    pass


class OrgExists(Exception):
    pass


class OrgService:
    def __init__(self) -> None:
        self._org = None
        self._org_repository = org_repository

    def get_all_members_in_org(self) -> list:
        """Gets a list of all of the members in the current organization

        Returns:
            [User]: A list of User-objects who are members in the current organisation
        """
        return self._org_repository.get_members(self._org.id)

    def get_orgs(self) -> list:
        """Gets all of the organisations where the logged in user is a member

        Returns:
            [Organisation]: A list of Organisation objects to which the current user belongs.
        """
        return user_service.get_current_user().organizations

    def join_org(self, code: str) -> Organization:
        """Adds a user to an organisation as a member

        Args:
            code (string):  The code used to join an organisation

        Raises:
            InvalidCode:    Raises this error if the given code doesn't belong to any organisation

        Returns:
            Organisation:   Returns an Organisation object of the organisation
                            to which the user was added.
        """
        org = self._org_repository.fetch_org(code)
        if not org:
            raise InvalidCode

        self._org_repository.add_to_org(
            user_service.get_current_user().id, org.id)
        user_service.get_current_user().organizations.append(org)
        self._org = org
        return org

    def create_org(self, name: str, code: str) -> Organization:
        """Creates a new organisation.

        Args:
            name (str): The organisation's name
            code (str): The code that others will use to join the organisation

        Raises:
            OrgExists: Raises this error if another organisation is already using the code

        Returns:
            Organisation: Returns an Organisation object of the newly created organisation.
        """
        if self._org_repository.fetch_org(code):
            raise OrgExists

        org = self._org_repository.create_org(
            name, code, user_service.get_current_user().id)
        user_service.get_current_user().organizations.append(org)
        self._org = org
        return org

    def get_current_org(self) -> Organization:
        """Returns the currently active organisation

        Returns:
            Organisations: An Organisation object of the currently activeOrganisation
        """
        return self._org

    def set_current_org(self, org: Organization):
        """Chenges the currently active organisation

        Args:
            org (Organization): An organisation object that will be set as the current organisation.
        """
        self._org = org

    def delete_org(self, org_id: int):
        """Deletes an organisation. Mainly used for testing purposes

        Args:
            org_id (int): The ID of the organisation that will be deleted.
        """
        self._org_repository.delete_org(org_id)

    def is_admin(self) -> bool:
        """Checks if the current user is an admin in the current organisation

        Returns:
            Bool: Is the user admin or not
        """
        return self._org_repository.is_admin(self._org.id, user_service.get_current_user().id)

    def make_admin_in_current_org(self, user: User):
        """Nominates a user to an admin status

        Args:
            user (User): The user that will be nominated to an admin status.
        """
        self._org_repository.add_as_admin(user.id, self._org.id)

    def signout(self):
        """Nullifies the current user.
        """
        self._org = None


org_service = OrgService()
