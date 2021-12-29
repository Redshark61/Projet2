import psycopg2
from db.mdp import mdp
from psycopg2.extensions import AsIs


class Database:
    """
    Class wich operate all the basic oparations with the database
    """

    connection = None
    # Try to connect at the first call of the class
    try:
        connection = psycopg2.connect(
            user="postgres",
            password=mdp,
            host="localhost",
            port="5432",
            database="projet2")

    except(psycopg2.Error) as error:
        print(f"Impossible de se connecter à la base Postgre 'projet2'\n{error}")

    @classmethod
    def disconnect(cls):
        """
        Disconnect the database
        """
        if cls.connection:
            cls.connection.close()

    @classmethod
    def query(cls, query: str, values: tuple = None, isTable: int = False) -> list[tuple]:
        """
        Execute a SQL query and return the result, NOne if the query is not an "Insert"
        """

        cursor = cls.connection.cursor()
        # If the value is a table, we need to use the AsIs function in order to remove the quotes '
        if isTable:
            cursor.execute(query, (AsIs(values[0]),))
        else:
            cursor.execute(query, values)

        if "SELECT" in query.upper():
            result = cursor.fetchall()
            return result
        cls.connection.commit()
        return None

    @staticmethod
    def getLastID(tableName: str) -> int:
        """
        Get the id of the required table
        """
        query = """
        SELECT id FROM %s
        ORDER BY id DESC
        LIMIT 1
        """
        id = Database.query(query, (tableName,), True)[0][0]

        return id
