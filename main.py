import csv
import os
from time import sleep
from subprocess import run
from cryptography.hazmat.primitives.asymmetric import rsa as Cipher
from cryptography.hazmat.primitives.asymmetric import dh as DH
from cryptography.hazmat.primitives.kdf import hkdf as HKDF

PATH_MEDIA = 'data/video1.mp4'


class Server:
	def __init__(self):
		self.privkey = Cipher.generate_private_key(public_exponent=65537, key_size=4096)
		self.pubkey = ""
		self.shrkey = ""

class Client:
	def __init__(self):
		self.privkey = Cipher.generate_private_key(public_exponent=65537, key_size=4096)
		self.pubkey = ""
		self.shrkey = ""


# Low budget authentication
def login():
	# TODO: Implement
	username = input("Enter username: ")
	password = input("Enter password: ")


def register():
	# TODO: Implement
	username = input("Enter username: ")
	password = input("Enter password: ")


def unregister():
	# TODO: Implement
	username = input("Enter username: ")
	password = input("Enter password: ")


def main():
	while (True):
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
				exit(0)
			case _:
				print("Invalid Option!")
				sleep(2)
				continue


# run(['python', 'vlcgui.py', PATH_MEDIA])


if __name__ == "__main__":
	main()
