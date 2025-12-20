import passworddb
import encrypter

def main():
    db = passworddb.Database()
    print("Welcome to the Password Manager!")
    while True:
        website = input("Enter the website (or 'exit' to quit): ")
        if website.lower() == 'exit':
            break
        salt = encrypter.generate_salt()
        
        master_password = encrypter.get_master_password()
        