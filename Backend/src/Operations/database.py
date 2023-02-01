import psycopg2

class Database:

    def __init__(self):
        self.conn = ""
        self.host = "localhost"
        self.name = "unbxddatabase"
        self.user = "unbxd"
        self.password = "unbxd"


    """
        Connect to the database
        Args: None
        Returns: cursor object to the connection
    """

    def connect_to_db(self):
        self.conn = psycopg2.connect(host=self.host, database=self.name, user=self.user, password=self.password)
        cur = self.conn.cursor()
        return self.conn, cur


    """
        Commit transaction and close the connection to a database
        Args: connection object conn, cursor object cur
        Returns: None
    """

    def close_db_connection(self, conn, cur):
        conn.commit()
        cur.close()
        conn.close()
        return


    def read_from_db(self, query, params_tuple=()):
        conn, cur = self.connect_to_db()

        try:
            print(params_tuple)
            cur.execute(query, params_tuple)
            data = cur.fetchall()
        except Exception as e:
            print(e)
            print("Transaction unsuccessful")
            return "Transaction unsuccesful"

        self.close_db_connection(conn, cur)

        return data


    def write_to_db(self, query, params_tuple):
        conn, cur = self.connect_to_db()
        
        try:
            
            cur.execute(query, params_tuple)
        except Exception as e:
            print(e)
            print("Transaction unsuccessful")
            return "Transaction unsuccessful"

        self.close_db_connection(conn, cur)
        return "Transaction successful" 


    def create_table(self, query):
        conn, cur = self.connect_to_db()
        
        try:
            cur.execute(query)
        except:
            return "Unable to create table"

        self.close_db_connection(conn, cur)
        return "Table created" 
