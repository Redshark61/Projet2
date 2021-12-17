import psycopg2


class Database:

    connection = None

    try:
        connection = psycopg2.connect(
            user="postgres",
            password="root",
            host="localhost",
            port="5432",
            database="projet2")

    except(psycopg2.Error) as error:
        print(f"Impossible de se connecter à la base Postgre 'projet2'\n{error}")

    @classmethod
    def disconnect(cls):
        if cls.connection:
            cls.connection.close()

    @classmethod
    def query(cls, query):
        cursor = cls.connection.cursor()
        cursor.execute(query)
        if "SELECT" in query:
            result = cursor.fetchall()
            return result
        cls.connection.commit()
        return None

    @staticmethod
    def getLastID(tableName):
        # Get the id of the last monster inserted
        query = f"""
        SELECT id FROM {tableName}
        ORDER BY id DESC
        LIMIT 1
        """
        id = Database.query(query)[0][0]

        return id
