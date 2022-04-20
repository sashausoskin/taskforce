from repositories.org_repository import org_repository
from user_service import user_service


class InvalidCode(Exception):
    pass


class OrgExists(Exception):
    pass


class OrgService:
    def __init__(self) -> None:
        self._org = None
        self._org_repository = org_repository

    def get_all_members_in_org(self):
        return self._org_repository.get_members(self._org.id)

    def get_orgs(self):
        return user_service.get_current_user().organizations

    def join_org(self, code):
        org = self._org_repository.fetch_org(code)
        if not org:
            raise InvalidCode

        self._org_repository.add_to_org(
            user_service.get_current_user().id, org.id)
        user_service.get_current_user().organizations.append(org)
        self._org = org
        return org

    def create_org(self, name, code):
        if self._org_repository.fetch_org(code):
            raise OrgExists

        org = self._org_repository.create_org(
            name, code, user_service.get_current_user().id)
        user_service.get_current_user().organizations.append(org)
        self._org = org
        return org

    def get_current_org(self):
        return self._org

    def set_current_org(self, org):
        self._org = org

    def delete_org(self, org_id):
        self._org_repository.delete_org(org_id)

    def is_admin(self):
        return self._org_repository.is_admin(self._org.id, user_service.get_current_user().id)

    def make_admin_in_current_org(self, user):
        self._org_repository.add_as_admin(user.id, self._org.id)

    def signout(self):
        self._org = None


org_service = OrgService()
