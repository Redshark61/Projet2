import psycopg2
from db.mdp import mdp


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
        print(
            f"Impossible de se connecter à la base Postgre 'projet2'\n{error}")

    @classmethod
    def disconnect(cls):
        """
        Disconnect the database
        """
        if cls.connection:
            cls.connection.close()

    @classmethod
    def query(cls, query: str) -> list[tuple] :
        """
        Execute a SQL query and return the result, NOne if the query is not an "Insert"
        """

        cursor = cls.connection.cursor()
        cursor.execute(query)
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
        query = f"""
        SELECT id FROM {tableName}
        ORDER BY id DESC
        LIMIT 1
        """
        id = Database.query(query)[0][0]

        return id
