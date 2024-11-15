import docker
import io
import os
import tarfile

class TaskManager:
    def __init__(self):
        try:
            print("Initializing Docker client...")
            self.client = docker.from_env()
        except Exception as e:
            print(f"Error initializing Docker client: {str(e)}")

    def process(self, code, language):
        image = self.get_docker_image(language)
        try:
            self.client.images.pull(image)
            
            container = self.client.containers.create(
                image=image,
                stdin_open=True,
            )
            
            # Start the container
            container.start()
            
            # Ensure the directory exists in the container
            container.exec_run("mkdir -p /tmp")
            
            # Write code to a temporary file
            code_file_path = f"/tmp/"
            
            if language == "java":
                code_file_path += "Main.java"
            elif language == "c":
                code_file_path += "main.c"
            elif language == "cpp":
                code_file_path += "main.cpp"
            elif language == "python":
                code_file_path += "main.py"
            elif language == "javascript":
                code_file_path += "main.js"
                
            with open(code_file_path, "w") as code_file:
                code_file.write(code)
            
            # Check if the file is created
            if not os.path.exists(code_file_path):
                return f"Error: File {code_file_path} was not created."
            
            # Create a tar archive of the code file
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                tar.add(code_file_path, arcname=os.path.basename(code_file_path))
            tar_stream.seek(0)
            
            # Put the tar archive into the container
            container.put_archive('/tmp', tar_stream)
            
            # Compile the code if necessary
            if language != "python" and language != "javascript":
                compile_command = self.get_compile_command(language, compile_code=True)
                exec_result = container.exec_run(compile_command)
                if exec_result.exit_code != 0:
                    print(f"Compilation error: {exec_result.output.decode('utf-8')}")
                    container.stop()
                    container.remove()
                    return f"Compilation error: {exec_result.output.decode('utf-8')}"
            
            # Execute the code
            execute_command = self.get_compile_command(language, compile_code=False)
            exec_result = container.exec_run(execute_command)
            
            return exec_result.output.decode("utf-8"), container.id
        
        except Exception as e:
           return f"Error: {str(e)}"
    
    def get_docker_image(self, language):
        images = {
            "python": "python:latest",
            "java": "openjdk:latest",
            "c": "gcc:latest",
            "cpp": "gcc:latest",
            "javascript": "node:latest",
        }
        return images.get(language, "python:3.12.7")
        
    def get_compile_command(self, language, compile_code):
        if compile_code:
            commands = {
                "java": "javac /tmp/Main.java",
                "c": "gcc /tmp/main.c -o /tmp/main",
                "cpp": "g++ /tmp/main.cpp -o /tmp/main",
            }
        else:
            commands = {
                "python": "python /tmp/main.py",
                "java": "java -cp /tmp Main",
                "c": "/tmp/main",
                "cpp": "/tmp/main",
                "javascript": "node /tmp/main.js",
            }
        return commands.get(language, "echo 'Unsupported language'")