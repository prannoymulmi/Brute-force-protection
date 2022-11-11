# Description

This is a scoped project of the ASMIS system for the queens medical system, which only accounts for preventing brute
force
password attacks that might occur for the login system.

# Getting Started 🚀

### Prerequisites
* <a href=https://www.python.org/downloads/release/python-360/> Python 3.6 or Greater</a>
* <a href=https://pip.pypa.io/en/stable/installation/> pip 21.3.1 or Greater</a>

After installing the requirements run the following commands in order
```bash
python -m venv . # creates python virtual environment for the project
source bin/activate # activates virtual environment, this is on mac
script bin/activate # This is for windows
pip -V  #Is used to check if the virtual environment is being used 
pip install -r requirements.txt # Install all required dependencies
./venv/bin/python python -m uvicorn main:app --reload # Runs the server
```

### Valid Users to test from in the UI

To use the API run the server and enter http://127.0.0.1:8000/api/v1/docs and the available endpoints will be displayed.

```json
{
  "username": "testUser1",
  "password": "V3ryG00dPassw0rd?!",
  "email": "hello@hello.com"
}
```

```bash
# Run unit test
python -m pytest tests/
```

## Dependency Injection

## Automated Tests

# Implemented security measures for ASMIS authentication system

* The usernames and password inputs have a max length of ```64 characters``` to prevent any kind of injection attacks.
* The passwords have to follow strict patterns of having at least ```16 characters, 2 digits, 2 Uppercase, 2 Lowercase, and 2 digits```.
This helps prevents staff from practicing poor password hygiene and makes brute force attacks harder.
* Passwords are stored using argon2id hashing algorithms which are resilient against side-channel and GPU attacks.
  Example ```$argon2id$v=19$m=65536,t=3,p=4$ngO2O3DDwuUuVttzpwIyWA$CjigQrhs4Yvh2cNd2/x/K4hhcZFuj1XCvWzHvcqxM08```(Add
  Reference)
* Used argon2 ```verify (hashed_password, to_be_verified_password)``` function to verify password instead of doing a
  string comparison, also prevents side-channel attacks.
* Used SQL Model functions ```select(User).where(User.username == username)``` which sanitizes the sql statements
  preventing SQL injection.
* The login attempt is validated and counted up till 5 times, then the user is blocked for 10 minutes.
* The timestamp of the last login attempt is also stored for auditing purposes.

# References

* Tutorial how to run fastapi in a local
  environment <a href=https://fastapi.tiangolo.com/tutorial/first-steps/ class="external-link" target="_blank">
  Fast API</a>.
* A sample fullstack project to build a API using fast
  API <a href=https://github.com/scionoftech/FastAPI-Full-Stack-Samples class="external-link" target="_blank">
  Github</a>.
* Tutorial how to implement and test SQLModel ORM to connect the database to the
  application <a href=https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#configure-the-in-memory-database>
  SQLMODEL</a>.