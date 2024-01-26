import MySQLdb

connection = MySQLdb.connect(
    host="localhost",
    port=5000,
    user="root",
    passwd="abc123"
)

databases = ["database1", "database2", "database3"]

try:
    with connection.cursor() as cursor:
        for db in databases:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
            print(f"Database '{db}' created.")

        source_db = "database1"
        cursor.execute(f"USE {source_db}")
        print(f"Using source database '{source_db}'.")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age INT
            )
        """)
        print("Table 'users' created.")

        # dummy data
        cursor.executemany("""
            INSERT INTO users (name, age) VALUES (%s, %s)
        """, [("Elon Musk", 52), ("Bill Gates", 68), ("Jeff Bezos", 60)])
        print("Sample data inserted.")

    connection.commit()
    print("Changes committed.")

    for target_db in databases[1:]:
        with connection.cursor() as target_cursor:
            target_cursor.execute(f"USE {target_db}")
            print(f"Using target database '{target_db}'.")
            
            target_cursor.execute("DROP TABLE IF EXISTS users")
            target_cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    age INT
                )
            """)
            print("Table 'users' created in target database.")

            target_cursor.execute(f"INSERT INTO users SELECT * FROM {source_db}.users")
            print("Data synchronized.")

            target_cursor.execute("SELECT * FROM users")
            print(f"Data in {target_db}:")
            for row in target_cursor.fetchall():
                print(row)
            
            print("Data consistency checked.")
    
    connection.commit()
    print("Changes committed in target databases.")

except Exception as e:
    print(f"Error: {e}")

finally:
    connection.close()
    print("Connection closed.")