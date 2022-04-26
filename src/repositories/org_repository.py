from entities.organization import Organization
from entities.user import User
from database_con import get_db_connection


class OrgRepository:

    def __init__(self, conn) -> None:
        self.conn = conn
        self._cursor = self.conn.cursor()

    def fetch_org(self, code: str):
        """Fetches an organisations information matching the code

        Args:
            code (str):     Code used to join an organisation

        Returns:
            Organisation:   An object of class Organisation
                            if there is an organisation matching the code.
            None:           If an organisation matching the code cannot be found
        """
        self._cursor.execute(
            "SELECT name, code, id FROM Organizations WHERE code=%s;", (code, ))
        results = self._cursor.fetchone()
        if not results:
            return None
        return Organization(results[0], results[1], results[2])

    def org_member(self, user_id: int):
        """
            Gets all of the organisations where a user is a member
        Args:
            user_id (integer):  ID of the user whose memberships want to be retrieved.

        Returns:
            [Organisation]:     Returns a list of Organisation-objects where a user is a member.
        """
        self._cursor.execute(
            """SELECT name, code, id FROM Organizations O LEFT JOIN OrgMembers OM ON OM.org=O.id
            WHERE OM.member=%s;""",
            (user_id, ))
        results = self._cursor.fetchall()
        orgs = []
        for result in results:
            orgs.append(Organization(result[0], result[1], result[2]))

        return orgs

    def add_to_org(self, user_id: int, org_id: int):
        """
            Adds a user to an organisation as a member.
        Args:
            user_id (integer):  ID of the user that is going to be added to the organisation
            org_id (_type_):    ID of the organisation where the user is going to be added

        Returns:
            Organisation:       Returns an object of class Organisation
                                with information on the organisation where the user was added.
        """
        self._cursor.execute(
            "INSERT INTO OrgMembers VALUES (%s, %s, FALSE);", (user_id, org_id))
        self.conn.commit()
        self._cursor.execute(
            "SELECT name, code, id FROM Organizations WHERE id=%s;", (org_id, ))
        results = self._cursor.fetchone()
        return Organization(results[0], results[1], results[2])

    def add_as_admin(self, user_id: int, org_id: int):
        """Promotes a user in an organisation to an admin status

        Args:
            user_id (integer):  ID of the user who is going to be promoted
            org_id (integer):   ID of the organisation where the user is going to be promoted
        """

        self._cursor.execute(
            "UPDATE OrgMembers SET admin=TRUE WHERE member=%s AND org=%s;", (user_id, org_id))
        self.conn.commit()

    def create_org(self, name: str, code: int, user_id: int):
        """Adds a brand new organisation in the database

        Args:
            name (string):      Name of the organisation
            code (string):      The code that others are going to use to join the organisation
            user_id (string):   ID of the user that is creating the organisation

        Returns:
            Organisation:       An object of the newly created organisation
        """

        self._cursor.execute(
            "INSERT INTO Organizations (name, code) VALUES (%s, %s);", (name, code))
        self.conn.commit()
        org = self.fetch_org(code)
        self.add_to_org(user_id, org.id)
        self.add_as_admin(user_id, org.id)
        return org

    def delete_org(self, org_id: int):
        """Deletes an organisation from the database. Mainly used for testing purposes.

        Args:
            org_id (integer): ID of the organisation that is going to be deleted.
        """

        self._cursor.execute(
            "DELETE FROM OrgMembers WHERE org=%s;", (org_id, ))

        self._cursor.execute(
            "DELETE FROM Organizations WHERE id=%s;", (org_id, ))

        self.conn.commit()

    def is_admin(self, org_id: int, user_id: int):
        """Checks whether or not a user has an admin status in an organisation

        Args:
            org_id (integer):   ID of the organisation where the check is done
            user_id (integer):  ID of the user on whom the check is done.

        Returns:
            Bool:               is the user admin in the organisation
        """
        self._cursor.execute(
            "SELECT admin FROM OrgMembers WHERE org=%s AND member=%s;", (
                org_id, user_id)
        )
        return self._cursor.fetchone()[0]

    def get_members(self, org_id: int):
        """Retrieves all of the users that are members in an organisation.
        Args:
            org_id(integer):    ID of the organisation where the users will be retrieved

        Returns:
            [User]:             A list of User objects who are members in the given organisation
        """
        self._cursor.execute(
            """SELECT U.name, U.username, U.id FROM Users U
            LEFT JOIN OrgMembers OM ON OM.member = U.id
            WHERE OM.org = %s AND admin=FALSE;""", (
                org_id, )
        )

        member_list = []

        for result in self._cursor.fetchall():
            member_list.append(User(result[0], result[1], "", result[2]))

        return member_list


org_repository = OrgRepository(get_db_connection())
