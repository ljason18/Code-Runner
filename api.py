from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import task_manager                   

app = FastAPI()
task_manager = task_manager.TaskManager()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1.8000",
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
    
@app.post("/compile")
async def compile(request: CompileRequest):
    task_id = uuid.uuid4()
    code = request.code
    language = request.language
    
    print("code: ", code)
    print("language: ", language)
    
    result = task_manager.process(request.code, request.language, task_id)
    print("result: ", result)
    return {"task_id": task_id, "result": result}