# Code Runner
## Project Description
A web-based code editor designed to compile and execute code directly in the browser. The program supports multiple programming languages without requiring users to install local compilers. It leverages Docker containers to fetch and run language-specific compiler images, ensuring a seamless and isolated execution environment. The output of the code is displayed immediately after execution. Currently, it only supports simple code that outputs results to standard output (stdout), such as text-based programs.

Languages supported: Java, C/C++, Python, JavaScript

The program enables syntax highlighting by utilizing a code editor from [CodeMirror](https://codemirror.net)
## Requirments
- Docker
    - This project is designed to run on a Linux distribution, not on Windows or Mac.
        - Once the program is running, the webpage can be accessed from any system.
    - The limitation is due to differences in Docker's socket/daemon communication mechanisms across operating systems

## Setup
Use ```docker compose up --build``` to build the latest version of the image.

Use ```docker compose up -d``` if image is already built

### Potential Error(s) and Debugging
#### Permission denied
Quick Fix: run ```getent group docker``` on your system and take note of the GID for the docker group. Then make sure that ```ARG GID``` in [Dockerfile](./backend/Dockerfile) is set to that GID.

To start debugging, start the container with ```docker compose -f compose.debug.yaml up --build```.

Then open a new terminal tab. And open up a shell inside the container with ```docker exec -it <containerID> /bin/bash```
- Replace containerID with the containerID of the the debug container
```
server-1  | Initializing Docker client...
server-1  | Error initializing Docker client: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))
```

In the shell, run ```ls -l /var/run/docker.sock```

Then run ```getent group docker```

If ls -l doesnt say docker for the group, and instead it outputs a GID. Then the GID of docker is not set properly, it should match the GID given in the ls -l command. If the getent command outputs a different GID for group docker,
then go to the [Dockerfile](./backend/Dockerfile) and set ```ARG GID``` to the GID that owns docker.sock
- The GID of the docker group can differ depending on your system

Example - GID given
```
appuser@fa3afecff2d8:/app$ ls -l /var/run/docker.sock
srw-rw---- 1 root 1000 0 Nov 13 04:01 /var/run/docker.sock
appuser@fa3afecff2d8:/app$ getent group docker
docker:x:999:appuser
```

Example - group docker
```
appuser@f05402a20850:/app$ ls -l /var/run/docker.sock
srw-rw---- 1 root docker 0 Nov 13 04:01 /var/run/docker.sock
```

## Using the project
Go to ```http://127.0.0.1:8080``` in your web browser as the project will be locally hosted on your system.
