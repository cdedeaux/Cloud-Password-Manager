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
        webpage = input("Enter the website: ")

        salt = encrypter.generate_salt()
        verification_hash = encrypter.get_verification_hash(master_password)
        db.add_verifications(salt, verification_hash)

        web_pass = input("Enter the password to encrypt: ")
        nonce, tag, encrypted_password = encrypter.create_encrypted_data(master_password, web_pass, salt)

        db.add_password(website, encrypted_password, nonce, tag)
        print(f"Password for {website} added successfully!")
if __name__ == "__main__":
    main()
