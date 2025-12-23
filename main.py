import passworddb
import encrypter
import decrypter
def main():
    db = passworddb.Database()
    print("Welcome to the Password Manager!")
    websites = db.get_password_list()
    while True:
        print("What would you like to do?")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. View all stored websites")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")
        match choice:
            case "1":
                for website in websites:
                    print(f" - {website}")
    
                website = input("Enter the website: ")
                salt = encrypter.generate_salt()

                master_password = encrypter.get_master_password()

                salt = encrypter.generate_salt()
                verification_hash = encrypter.get_verification_hash(master_password)
                db.add_verifications(salt, verification_hash)

                web_pass = input("Enter the password to encrypt: ")
                nonce, tag, encrypted_password = encrypter.create_encrypted_data(master_password, web_pass, salt)

                db.add_password(website, encrypted_password, nonce, tag)
                print(f"Password for {website} added successfully!")
            case "2":
                for website in websites:
                    print(f" - {website}")
    
                website = input("Enter the website to retrieve the password for: ")
                decryption_data = db.get_decryption_data(website)
                if decryption_data:
                    ciphertext, nonce, tag = decryption_data
                    salt = db.get_user_salt()
                    master_password = encrypter.get_master_password()
                    encryption_key = decrypter.derive_encryption_key(master_password, salt)
                    password = decrypter.decrypt_password(encryption_key, ciphertext, nonce, tag)
                    if password:
                        print(f"The password for {website} is: {password}")
            case "3":
                print("Stored websites:")
                for website in websites:
                    print(f" - {website}")
            case "4":
                print("Exiting Password Manager. Goodbye!")
                break
                



if __name__ == "__main__":
    main()
