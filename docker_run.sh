#!/bin/bash

# Run docker with port forwarding and attach to bash
# set container id
docker run --name yolov8-fastapi -it --rm -p 8061:8061 yolov8-fastapi:latest

# docker run -it --rm -p 8061:8061 -v ./app:/code/app  yolov8-fastapi:latest

exit

## How to attach
docker exec -it yolov8-fastapi /bin/bash

uvicorn app.main:app --host 0.0.0.0 --port 8061 --reload