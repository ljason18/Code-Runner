# Description: This is a simple python script that prints "Hello World" to the console.
# Used to get the docker container running if you have issues with docker compose.
from fastapi import FastAPI

app = FastAPI()

app.get("/")
def read_root():
    return {"Hello": "World"}