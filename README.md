# Web-Compiler
## Project Description
An implementation of a web compiler used to compile code directly without the need to use an IDE or terminal. Allows for compiling code for different languages without requiring users to have the corresponding compilers installed. Utilizes docker containers to retrieve the corresponding docker image for each language compiler.

Languages supported: Java, C/C++, Python

## Requirments
- docker

## Setup
Use ```docker compose up --build``` to build the latest version of the image.

Use ```docker compose up -d``` if image is already built

### Potential Errors and Debugging
To start debugging, start the container with ```docker compose -f compose.yaml -f compose.debug.yaml up --build```.

Then open a new terminal tab. And open up a shell inside the container with ```docker exec -it <containerID> /bin/bash```
- Replace <containerID> with the containerID of the the server container

#### Permission denied
```
server-1  | Initializing Docker client...
server-1  | Error initializing Docker client: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))
```

In the shell, run ```ls -l /var/run/docker.sock```

If the output is the following then you need to update the ownership of the docker socket. The default ownership should be root:docker however if its root:root, then you need to change it.
```
appuser@741c7064c66c:/app$ ls -l /var/run/docker.sock
srw-rw---- 1 root root 0 Nov 13 01:58 /var/run/docker.sock
```

## Using the project
Go to ```http://127.0.0.1:8000``` in your web browser as the project will be locally hosted on your system.
