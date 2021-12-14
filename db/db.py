import psycopg2


class Database:

    connection = None

    @classmethod
    def connect(cls, DBName):
        try:
            cls.connection = psycopg2.connect(
                user="postgres",
                password="Zarole28",
                host="localhost",
                port="5432",
                database=DBName)

        except(psycopg2.Error) as error:
            print(f"Impossible de se connecter à la base Postgre {DBName}\n{error}")

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
