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
        cur.execute("CREATE TABLE IF NOT EXISTS encrypted_passwords(website, ciphertext TEXT UNIQUE, nonce BLOB, tag BLOB)")
        self.connection.commit()
        self.connection.close()
    def add_password(self, website, encrypted_password, nonce, tag):
        try:
            self.connection = sqlite3.connect(self.db_name)
            cur = self.connection.cursor()
            cur.execute("INSERT INTO encrypted_passwords(website, password, nonce, tag) VALUES (?, ?, ?, ?)", (website, encrypted_password, nonce, tag))
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
            print("User data already exists in the database.")
        finally:
            self.connection.close()
    def get_decryption_data(self, website, db_name='encrypted_passwords.db'):
        try:
            self.connection = sqlite3.connect(db_name)
            cur = self.connection.cursor()
            cur.execute("SELECT ciphertextgit , nonce, tag FROM encrypted_passwords WHERE website=?", (website,))
            result = cur.fetchone()
            if result:
                return result
            else:
                print("No data found for the specified website.")
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.connection.close()
    def get_user_salt(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            cur = self.connection.cursor()
            cur.execute("SELECT salt FROM user_data")
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                print("No user salt found in the database.")
                return None
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.connection.close()
db = Database()
print("Database created successfully!")
