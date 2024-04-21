import pathlib
import platform
import subprocess
from cryptography.hazmat.primitives.asymmetric import rsa as Cipher
from cryptography.hazmat.primitives.asymmetric import dh as DH
from cryptography.hazmat.primitives.kdf import hkdf as HKDF

PATH_MEDIA = 'data/video1.mp4'

class Server():
	def __init__(self):
		privkey = Cipher.generate_private_key(public_exponent=65537,key_size=4096)
		pubkey = ""
		shrkey = ""

class Client():
	def __init__(self):
		self.privkey = Cipher.generate_private_key(public_exponent=65537,key_size=4096)
		self.pubkey = ""
		self.shrkey = ""


def main():
	subprocess.run(['python', 'vlcgui.py', PATH_MEDIA])
	print("Hi")


if __name__ == "__main__":
	main()

