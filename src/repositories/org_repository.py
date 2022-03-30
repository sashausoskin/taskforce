from entities.organization import Organization
from database_con import get_db_connection

class OrgRepository:

    def __init__(self, conn) -> None:
        self.conn = conn
        self._cursor = self.conn.cursor()
    
    def fetch_org(self, code):
        self._cursor.execute("SELECT name, code, id FROM Organizations WHERE code=%s", (code, ))
        results = self._cursor.fetchone()
        if not results:
            return None
        return Organization(results[0], results[1], results[2])
    
    def org_member(self, user_id):
        self._cursor.execute("SELECT name, code, id FROM Organizations O LEFT JOIN OrgMembers OM ON OM.org=O.id WHERE OM.member=%s", (user_id, ))
        results = self._cursor.fetchall()
        orgs = []
        for result in results:
            orgs.append(Organization(result[0], result[1], result[2]))
        
        return orgs
    
    def add_to_org(self, user_id, org_id):
        self._cursor.execute("INSERT INTO OrgMembers VALUES (%s, %s, FALSE)", (user_id, org_id))
        self.conn.commit()
        self._cursor.execute("SELECT name, code, id FROM Organizations WHERE id=%s", (org_id, ))
        results = self._cursor.fetchone()
        return Organization(results[0], results[1], results[2])
    
    def add_as_admin(self, user_id, org_id):
        self._cursor.execute("UPDATE OrgMembers SET admin=TRUE WHERE member=%s AND org=%s", (user_id, org_id))
    
    def create_org(self, name, code, user_id):
        self._cursor.execute("INSERT INTO Organizations (name, code) VALUES (%s, %s)", (name, code))
        self.conn.commit()
        org = self.fetch_org(code)
        self.add_to_org(user_id, org.id)
        self.add_as_admin(user_id, org.id)
        return org

        
org_repository = OrgRepository(get_db_connection())