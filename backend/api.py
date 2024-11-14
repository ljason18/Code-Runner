from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import task_manager as task_manager

app = FastAPI()
task_manager = task_manager.TaskManager()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompileRequest(BaseModel):
    code: str
    language : str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the backend API!"}

@app.post("/compile")
async def compile(request: CompileRequest):
    result = task_manager.process(request.code, request.language)
    print("result: ", result)
    return {"result": result}