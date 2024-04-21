import pathlib
import platform
import subprocess
from cryptography.hazmat.primitives.asymmetric import rsa as Cipher
from cryptography.hazmat.primitives.asymmetric import dh as DH
from cryptography.hazmat.primitives.kdf import hkdf as HKDF

PATH_ROOT = pathlib.Path(__file__).resolve().parent.parent
PATH_VLC = f'{PATH_ROOT}/src/vlcgui.py'
PATH_VENV = f'{PATH_ROOT}/src/vlcgui.py'
PATH_MEDIA = ''

class Server:
	def __init__(self):
		privkey = Cipher.generate_private_key(public_exponent=65537,key_size=4096)
		pubkey = ""
		shrkey = ""

class Client:
	def __init__(self):
		self.privkey = Cipher.generate_private_key(public_exponent=65537,key_size=4096)
		self.pubkey = ""
		self.shrkey = ""


def main():
	subprocess.run(['python', PATH_VLC, PATH_MEDIA])


if __name__ == "__main__":
	main()
