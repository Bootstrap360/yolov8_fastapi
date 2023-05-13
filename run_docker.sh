#!/bin/bash

docker build -t yolov8-fastapi .

# Run docker with port forwarding and attach to bash

docker run -it --rm -p 8061:8061 yolov8-fastapi