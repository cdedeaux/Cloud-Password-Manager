import sqlite3
import sys

class Database:
    def __init__(self, db_name='ips.db'):
        self.db_name = db_name
        try:
            self.connection = sqlite3.connect(self.db_name)
        except:
            print("Failed database connection.")
            sys.exit()
        
        cur = self.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS ip(ip_address TEXT UNIQUE)")
        self.connection.commit()
        self.connection.close()

# Create the database
db = Database()
print("Database created successfully!")
