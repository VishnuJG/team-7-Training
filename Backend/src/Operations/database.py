import psycopg2

class Database:

    def __init__(self):
        self.conn = ""
        # self.host = "db-container"
        self.host = "localhost"
        # self.name = "unbxddb-container"
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


    """
        Read operation from the database
        Args: query to be executed
              tuple of parameters for the query 
        Returns: list
    """

    def read_from_db(self, query, params_tuple=()):

        conn, cur = self.connect_to_db()

        try:
            cur.execute(query, params_tuple)
            data = cur.fetchall()
        except Exception as e:
            print(e)
            return "Error: " + str(e)
            
        self.close_db_connection(conn, cur)
        return data


    """
        Write operation to the database
        Args: query to be executed
              tuple of parameters for the query 
        Returns: status message
    """

    def write_to_db(self, query, params_tuple):
        conn, cur = self.connect_to_db()
        
        try:
            
            cur.execute(query, params_tuple)
        except Exception as e:
            print(e)
            return "Error: " + str(e)

        self.close_db_connection(conn, cur)
        return "Success"


    """
        Create a table in the database
        Args: query to be executed
        Returns: status message
    """
    def create_table(self, query):
        conn, cur = self.connect_to_db()
        
        try:
            cur.execute(query)
        except Exception as e:
            print(e)
            return "Error: " + str(e)

        self.close_db_connection(conn, cur)
        return "Success"
