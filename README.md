# Starting the project

## Creating a python virtual environment
This is done using python3  so please make sure that python3 is installed before executing the commands to install the 
dependencies.

```
1. python -m venv .
2. source bin/activate
3. pip -V  #Is used to check if the virtual environment is being used 
4. pip install -r requirements.txt
5. ./venv/bin/python python -m uvicorn main:app --reload 
```

## References
* Tutorial how to run fastapi in a local environment <a href=https://fastapi.tiangolo.com/tutorial/first-steps/ class="external-link" target="_blank">
Fast API</a>.
* A sample fullstack project to build a API using fast API <a href=https://github.com/scionoftech/FastAPI-Full-Stack-Samples class="external-link" target="_blank">
Github</a>.