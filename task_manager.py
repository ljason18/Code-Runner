import docker

class TaskManager:
    def __init__(self):
        self.client = docker.from_env()
        
    def process(self, code, language, task_id):
        image = self.get_docker_image(language)
        
        try:
            self.client.images.pull(image)
            
            container = self.client.containers.create(
                image=image,
                command=self.get_compile_command(language, code),
                stdin_open=True,
            )
            
            container.start()
            logs = container.logs(stream=False)
            container.remove()
            return logs.decode("utf-8")
        
        except Exception as e:
           return f"Error: {str(e)}"
    
    def get_docker_image(self, language):
        images = {
            "python": "python:latest",
            "java": "openjdk:latest",
            "c": "gcc:latest",
            "cpp": "gcc:latest",
        }
        return images.get(language, "python:3.12.7")
        
    def get_compile_command(self, language, code):
        commands = {
            "python": f"echo '{code}' > code.py | python code.py",
            "java": f"echo '{code}' > Main.java && javac Main.java && java Main",
            "c": f"echo '{code}' > main.c && gcc main.c -o main && ./main",
            "cpp": f"echo '{code}' > main.cpp && g++ main.cpp -o main && ./main",
        }
        return commands.get(language, "echo 'Unsupported language'")