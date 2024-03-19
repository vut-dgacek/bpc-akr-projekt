# bpc-akr-projekt

## Install

Windows:

- Rename `install.txt` to `install.ps1`
- Run: `Set-ExecutionPolicy RemoteSigned -Scope process`
- Run: `install.ps1`

Linux:

- Rename `install.txt` to `install.sh`
- Run: `install.sh`


## Run

Windows:

- Rename: `run-client.txt` to `run-client.ps1`
- Run: `Set-ExecutionPolicy RemoteSigned -Scope process`
- Run: `run-client.ps1`


Linux:

- Rename: `run-client.txt` to `run-client.sh`
- Run: `run-client.sh`


## Dumping dependencies

- Be inside active venv
- Run: `pip freeze > requirements.txt`

