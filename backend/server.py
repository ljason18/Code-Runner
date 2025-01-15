from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import task_manager as task_manager

app = FastAPI()
task_manager = task_manager.TaskManager()

origins = [
    "http://localhost:8080",
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
    input: str

def clean_up(container):
    try:
        container.stop()
        container.remove()
    except Exception as e:
        print(f"Error cleaning up container: {str(e)}")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the backend API!"}

@app.post("/compile")
async def compile(request: CompileRequest, background_tasks: BackgroundTasks):
    result, containerID = task_manager.process(request.code, request.language, request.input)
    background_tasks.add_task(clean_up, task_manager.client.containers.get(containerID))
    return {"result": result}