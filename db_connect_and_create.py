import mysql.connector
from mysql.connector import Error

def get_db_connection():
    db_name = "fitness_center"
    user = "root"
    password = "[insert your password]"
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user=user,
            password=password,
            host=host
        )

        if conn.is_connected():
            print ("Connected to MySQL database successfully")
            return conn
        
    except Error as e:
        print(f"Error: {e}")
        return None
    
def create_tables():
    conn = get_db_connection()
    if conn is not None:
        try:
            cursor=conn.cursor()
            query =   """
                CREATE TABLE Members (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NULL
                );
                CREATE TABLE WorkoutSessions (
                session_id INT AUTO_INCREMENT PRIMARY KEY,
                member_id INT NOT NULL,
                date DATETIME NOT NULL,
                duration_minutes VARCHAR(25) NOT NULL,
                calories_burned VARCHAR(25) NOT NULL,
                FOREIGN KEY (member_id) REFERENCES Members(id)
                )
                """
            cursor.execute(query)
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                print("MySQL connection is closed.")
