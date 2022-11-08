# Description 
This is a scoped project of the ASMIS system for the queens medical system, which only accounts for preventing brute force 
password attacks that might occur for the login system. 

# Getting Started 🚀
The Instructions to get the project up and running.

## Creating a python virtual environment 🔧
This is done using python3  so please make sure that python3 is installed before executing the commands to install the 
dependencies.

```bash
python -m venv .
source bin/activate
pip -V  #Is used to check if the virtual environment is being used 
pip install -r requirements.txt
./venv/bin/python python -m uvicorn main:app --reload 
```

# Run unit test
```bash
python -m pytest tests/
```

## Implemented security measures for ASMIS authentication system
* The usernames and password inputs have a max length of 64 characters to prevent any kind of injection attacks.
* Passwords are stored using argon2id hashing algorithms which are resilient against side-channel and GPU attacks.(Add Reference)
* Using argon2 verify safe function to verify password instead of doing a string comparison. This helps secure the system from side channel attacks.
* The login attempt is validated and counted up till 5 times, then the user is blocked for 10 minutes. 

## References
* Tutorial how to run fastapi in a local environment <a href=https://fastapi.tiangolo.com/tutorial/first-steps/ class="external-link" target="_blank">
Fast API</a>.
* A sample fullstack project to build a API using fast API <a href=https://github.com/scionoftech/FastAPI-Full-Stack-Samples class="external-link" target="_blank">
Github</a>.