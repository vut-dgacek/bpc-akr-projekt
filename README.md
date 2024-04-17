# bpc-akr-projekt

## Install

Windows:

- Rename `install.txt` to `install.ps1`
- Run: `Set-ExecutionPolicy Unrestricted -Scope process`
- Run: `install.ps1`

Linux:

- Rename `install.txt` to `install.sh`
- Run: `install.sh`
- If you are running different shell than bash run: `bash install.sh`


## Run

Windows:

- Rename: `client.txt` to `client.ps1`
- Run: `Set-ExecutionPolicy Unrestricted -Scope process`
- Run: `client.ps1`


Linux:

- Rename: `client.txt` to `client.sh`
- Run: `client.sh`
- If you are running different shell than bash run: `bash client.sh`


## Dumping dependencies

- Be inside active venv
- Run: `pip freeze > requirements.txt`

