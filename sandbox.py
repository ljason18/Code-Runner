container = client.containers.run(
    image="gcc:latest",
    command=["/bin/sh", "-c", "echo 'int main() { return 0; }' | gcc -o myapp"],
    mem_limit="128m",
    cpu_shares=256,
    network_disabled=True,
    detach=True,
)
