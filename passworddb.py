import sqlite3
import sys

class Database:
    def __init__(self, db_name='encrypted_passwords.db'):
        self.db_name = db_name
        try:
            self.connection = sqlite3.connect(self.db_name)
        except:
            print("Failed database connection.")
            sys.exit()
        
        cur = self.connection.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS encrypted_passwords(website, password TEXT UNIQUE)")
        self.connection.commit()
        self.connection.close()
    def add_password(self, website, encrypted_password):
        try:
            self.connection = sqlite3.connect(self.db_name)
            cur = self.connection.cursor()
            cur.execute("INSERT INTO encrypted_passwords(website, password) VALUES (?, ?)", (website, encrypted_password,))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Password already exists in the database.")
        finally:
            self.connection.close()
    def add_verifications(self, salt, verification_hash):
        try:
            self.connection = sqlite3.connect(self.db_name)
            cur = self.connection.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS user_data(verification_hash TEXT UNIQUE,salt BLOB UNIQUE)")
            cur.execute("SELECT COUNT(*) FROM user_data")
            if (cur.fetchone()[0] > 0):
                print("User data already exists in the database.")
                return
            cur.execute("INSERT INTO user_data(verification_hash, salt) VALUES (?, ?)", (verification_hash, salt))
            self.connection.commit()
        except sqlite3.IntegrityError:
            print("Salt already exists in the database.")
        finally:
            self.connection.close()
db = Database()
print("Database created successfully!")
