import os
import csv
import base64
import hashlib
from time import sleep
from pathlib import Path
from subprocess import run
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# Below this line lies spaghetti code, good luck with reading it
# Cleanup stuff
def cleanup_tempdir():
	folder = 'data/tmp'
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path):
				os.remove(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))


def cleanup_encrypted_file(filename):
	folder = 'data/enc'
	file_path = os.path.join(folder, filename)
	try:
		if os.path.isfile(file_path):
			os.remove(file_path)
	except Exception as e:
		print('Failed to delete %s. Reason: %s' % (file_path, e))


# Databse manipulation
class DB:
	def __init__(self, username, password, file_path_to_encrypt):
		# Due to the fact that users will put anything into this variables, I've decided to base64 encode it so it
		# doesn't mess up the database
		self.username = base64.b64encode(bytes(username, "utf-8")).decode()
		self.password = hashlib.sha224(password.encode("utf-8")).hexdigest()
		self.user_key = AESGCM.generate_key(bit_length=128)
		self.file_hash = ""
		self.file_path_to_encrypt = file_path_to_encrypt
		self.dbpath = "data/users.csv"
		self.tempdbpath = "data/users.csv.tmp"
		self.file_extension = Path(file_path_to_encrypt).suffix

	def read(self):
		with open(self.dbpath, mode='r', newline='\n', encoding='utf-8') as file:
			data = []
			reader = csv.reader(file)
			# Data format: username, password, key, allowed_path(file_hash)
			# Read data
			for row in reader:
				data.append(row)
		return data

	def encrypt_media(self):
		# I know nonce should not be hardcoded nor used multiple times, however for the simplicity I'll hard code it - Dawid
		nonce = b"\xf6'M\x1f\x04&\x99h\xf1\x07\x94-f\xd8.\xf9\x9d\xa7\xa1\xa7\xcf$\x8b\x9f\xbe\x0e\x85\xdfx\xeei\x1c"

		# Check if 'file_path_to_encrypt' leads to file
		if os.path.isfile(self.file_path_to_encrypt):
			# Check if file is not empty
			if os.path.getsize(self.file_path_to_encrypt) > 0:
				# SHA224 digest is used as a filename
				with open(self.file_path_to_encrypt, 'rb', buffering=0) as file:
					self.file_hash = hashlib.file_digest(file, 'sha224').hexdigest()

				full_file_name = self.file_hash + Path(self.file_path_to_encrypt).suffix

				# Check if file already exists
				if not os.path.isfile(f'data/enc/{full_file_name}'):
					aesgcm = AESGCM(self.user_key)

					# Read file
					with open(self.file_path_to_encrypt, 'rb', buffering=0) as original:
						data = original.read()
					# Encrypt data
					ct = aesgcm.encrypt(nonce, data, None)

					# Save file
					with open(f'data/enc/{full_file_name}', 'wb', buffering=0) as encrypted:
						enc = encrypted.write(ct)
						print("# INFO: FILE HAS BEEN ENCRYPTED!")
				else:
					print("# ERROR: ENCRYPTED FILE EXISTS! EXITING!")
					exit(1)
			else:
				print("# ERROR: FILE IS EMPTY! EXITING!")
				exit(1)
		else:
			print("# ERROR: INVALID PATH! EXITING!")
			exit(1)

	def decrypt_media(self, key, filename):
		# I know nonce should not be hardcoded nor used multiple times, however for the simplicity I'll hard code it - Dawid
		nonce = b"\xf6'M\x1f\x04&\x99h\xf1\x07\x94-f\xd8.\xf9\x9d\xa7\xa1\xa7\xcf$\x8b\x9f\xbe\x0e\x85\xdfx\xeei\x1c"
		decoded_key = bytes(base64.b64decode(key))

		aesgcm = AESGCM(decoded_key)

		# Read file
		with open(f'data/enc/{filename}', 'rb', buffering=0) as original:
			data = original.read()
		# Encrypt data
		ct = aesgcm.decrypt(nonce, data, None)

		# Save file
		with open(f'data/tmp/{filename}', 'wb', buffering=0) as encrypted:
			enc = encrypted.write(ct)

		return f'data/tmp/{filename}'

	def authenticate_user(self):
		if os.path.getsize(self.dbpath) > 0:
			for row in self.read():
				if self.username != str(row[0]) or self.password != str(row[1]):
					print("# ERROR: WRONG USERNAME OR PASSWORD! EXITING!")
					exit(1)
				else:
					self.decrypt_media(str(row[2]), str(row[3]))
					run(['python', 'vlcgui.py', self.decrypt_media(str(row[2]), str(row[3]))])
		else:
			print("# ERROR: DATABASE IS EMPTY! EXITING!")
			exit(1)

	def append_user(self):
		with open(self.dbpath, 'r', newline='\n', encoding='utf-8') as database:
			with open(self.tempdbpath, 'w', newline='\n', encoding='utf-8') as tempdatabase:
				reader = csv.reader(database)
				writer = csv.writer(tempdatabase)
				# Check if file is empty
				if os.path.getsize(self.dbpath) > 0:
					for row in reader:
						# If credentials from old file do NOT match current credentials, write to new file
						if not str(base64.b64decode(self.username).decode()) == str(row[0]):
							if not self.password == str(row[1]):
								writer.writerow(row)
						else:
							print("# ERROR: USER ALREADY EXISTS! EXITING!")
							exit(1)
				else:
					# Encrypt media
					self.encrypt_media()

					full_file_name = self.file_hash + self.file_extension

					# Write credentials to new file
					writer.writerow([self.username, self.password, base64.b64encode(self.user_key).decode(), full_file_name])

		print("# INFO: USER HAS BEEN ADDED!")

		# Check if tempfile exist
		if os.path.isfile(self.tempdbpath):
			os.replace(self.tempdbpath, self.dbpath)

	def remove_user(self):
		# Find encrypted file and delete it
		for row in self.read():
			# If username and password match proceed with deletion
			if self.username == str(row[0]) and self.password == str(row[1]):
				cleanup_encrypted_file(str(row[3]))
				print(f'INFO: FILE data/enc/{str(row[3])} HAS BEEN DELETED!')

		if os.stat(self.dbpath).st_size != 0:
			with open(self.dbpath, 'r', newline='\n', encoding='utf-8') as database:
				with open(self.tempdbpath, 'w', newline='\n', encoding='utf-8') as tempdatabase:
					reader = csv.reader(database)
					writer = csv.writer(tempdatabase)
					for row in reader:
						# If credentials from old file do NOT match current credentials, write to new file
						if not str(base64.b64decode(self.username).decode()) == str(row[0]):
							if not self.password == str(row[1]):
								writer.writerow(row)
			# Check if tempfile exist
			if os.path.isfile(self.tempdbpath):
				os.replace(self.tempdbpath, self.dbpath)
		else:
			print("# ERROR: DATABASE IS EMPTY! EXITING!")
			exit(1)


def login():
	print("#==============================================================#")
	print("# Login:                                                       #")
	username = input("#     Enter username: ")
	password = input("#     Enter password: ")
	db = DB(username, password, "")
	db.authenticate_user()


def register():
	print("#==============================================================#")
	print("# Register user:                                               #")
	username = input("#     Enter username: ")
	password = input("#     Enter password: ")
	print("# WARNING: For file encryption you can use only included samples.")
	print("# Example: data/samples/sample-9s.mp3")
	file_to_encrypt = input("#     Enter file path to encrypt: ")
	db = DB(username, password, file_to_encrypt)
	db.append_user()


def unregister():
	print("#==============================================================#")
	print("# Delete user:                                                 #")
	username = input("#     Enter username: ")
	password = input("#     Enter password: ")
	db = DB(username, password, "")
	db.remove_user()


def main():
	while True:
		print("#==============================================================#")
		print("#              Low Budget \"\"\"Streaming\"\"\" Server               #")
		print("#==============================================================#")
		print("# Options:")
		print("#     1. Login")
		print("#     2. Register User")
		print("#     3. Delete User")
		print("#     4. Exit")
		print("#==============================================================#")
		useropt = input("Select option: ")
		match useropt:
			case "1":
				login()
				break
			case "2":
				register()
				break
			case "3":
				unregister()
				break
			case "4":
				cleanup_tempdir()
				exit(0)
			case _:
				print("# WARNING: INVALID OPTION!")
				sleep(2)
				continue


if __name__ == "__main__":
	try:
		main()
	finally:
		# Cleanup temporary database if exists
		if os.path.isfile("data/users.csv.tmp"):
			os.remove("data/users.csv.tmp")
