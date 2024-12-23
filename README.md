# Code Runner
## Project Description
A web-based code editor designed to compile and execute code directly in the browser. The program supports multiple programming languages without requiring users to install local compilers. It leverages Docker containers to fetch and run language-specific compiler images, ensuring a seamless and isolated execution environment. The output of the code is displayed immediately after execution. Currently, it only supports simple code that outputs results to standard output (stdout), such as text-based programs.

Languages supported: Java, C/C++, Python, JavaScript

The program enables syntax highlighting by utilizing a code editor from [CodeMirror](https://codemirror.net)

## Development Scope
This project is currently configured for **local development only**. Key aspects are:
- CORS Policy: Requests are restricted to localhost (127.0.0.1)
- Protocol: Uses HTTP instead of HTTPS.
- Connection Handling: The backend accepts connections from any source; however, due to the CORS policy, the frontend can only communicate with the backend through localhost.

### Production Readiness
Before deployment, the following changes will be required:
- Enable Secure Communication: Use HTTPS with a valid SSL/TLS certificate.
- Reconfigure CORS: Update the policy to allow requests from trusted origins.
- Strengthen Security: Implement authentication and access controls to safeguard the application.

## Requirments
- Docker
    - This project is designed to run/host on a Linux distribution
        - Currernt setup will not host properly on Windows systems.
        - Hosting on macOS is untested
    - The project is run inside a Docker container and attempts to communicate with the Docker socket/daemon on the host system. This means the socket must be mounted to the container.
    - The container is a Linux container which uses Unix domain sockets. However, Windows uses named pipes instead of Unix sockets. Named pipes don’t have explicit permissions, which prevents a non-privileged user from communicating with the Docker socket when the host system is Windows.
    - macOS should work similarly to Linux because it uses Unix domain sockets. However, performance is untested as I don't have access to a Mac system or VM.

## Setup
Use ```docker compose up --build``` to build the latest version of the image.

Use ```docker compose up -d``` if image is already built

### Potential Error(s) and Debugging
#### Permission denied
```
server-1  | Initializing Docker client...
server-1  | Error initializing Docker client: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))
```
Quick Fix: run ```getent group docker``` on your system and take note of the GID for the docker group. Then make sure that ```ARG GID``` in [Dockerfile](./backend/Dockerfile) is set to that GID.

##### Further Explanation
Since the GID of the docker group is system-dependent, the GID used in the Dockerfile is might differ from the one on the host system.

To start debugging, start the container with ```docker compose -f compose.debug.yaml up --build```.

Then open a new terminal tab and access a shell inside the container with ```docker exec -it <containerID> /bin/bash```
- Replace containerID with the containerID of the the debug container

In the shell, run ```ls -l /var/run/docker.sock```

Then run ```getent group docker```

Check the output of the ```ls``` command for the group that owns the socket.
- If a value is displayed, and it doesnt match the GID of the ```docker``` group, go to the [Dockerfile](./backend/Dockerfile) and set ```ARG GID``` to the GID that owns docker.sock

Example
```
appuser@fa3afecff2d8:/app$ ls -l /var/run/docker.sock
srw-rw---- 1 root 1000 0 Nov 13 04:01 /var/run/docker.sock
appuser@fa3afecff2d8:/app$ getent group docker
docker:x:999:appuser
```


## Using the project
Go to ```http://127.0.0.1:8080``` in your web browser as the project will be locally hosted on your system.
