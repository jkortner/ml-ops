# Sandbox

## Theia

Theia is an IDE that can be run in a Docker container. The script below pulls the image and runs the container.

```zsh
docker run -it --init -p 3000:3000 -v "$(pwd):/home/project:cached" theiaide/theia:latest
```

The Theia IDE should run on http://localhost:3000.

Theia can also be run for Python development. 

```zsh
docker run -it --init -p 3000:3000 -v "$(pwd):/home/project" theiaide/theia-python:latest
```