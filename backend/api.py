from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import task_manager as task_manager
import webbrowser
import os   

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

def launch_frontend():
    # Path to the frontend directory (adjust this path as needed)
    frontend_path = os.path.join(os.getcwd(), "index.html")

    # Option 1: If you want to launch a local server for the frontend (e.g., with Python's http.server)
    # subprocess.Popen(["python", "-m", "http.server", "--directory", "frontend", "8080"])

    # Option 2: If the frontend is served via a live server (use a browser)
    # Automatically open the frontend in the default browser
    webbrowser.open("http://localhost:8080")  # Adjust URL based on your frontend server

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