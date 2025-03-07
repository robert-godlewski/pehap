# This is file is used to handle interaction with the db
import sqlite3


class DBConnection:
    def __init__(self, db_name: str) -> None:
        self.connection = sqlite3.connect(db_name)

    def query_db(self, query, data=None):
        cursor = self.connection.cursor()
        db_ok = True
        try:
            print("Running Query:", query)
            print(type(query))
            if data:
                cursor.execute(query, data)
                result = cursor.fetchall()
            else:
                cursor.executescript(query)
                result = True
            return result
        except Exception as e:
            print("Something went wrong:", e)
            db_ok = False
            return db_ok
        finally:
            if db_ok:
                self.connection.commit()
            self.connection.close()


# Function is used to create an instance of the DBConnection
def connectToDB(db_name: str) -> DBConnection:
    return DBConnection(db_name)
