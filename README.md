# yolov8 FastAPI Server

This project contains minimal code to run a yolov8 model on a FastAPI server.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


Clone the repository and navigate to the project directory.

```bash
git clone git@github.com:Bootstrap360/yolov8_fastapi.git
cd yolov8_fastapi
```

To build and run the docker image, run the following command.

```bash
bash docker_build.sh
bash docker_run.sh
```

The server should now be running on `http://localhost:8061`.

To test the server, you need to install demo requirements.

```bash
pip install -r requirements_demo.txt
```

Then run the following command to test the server.

```bash
python demo.py
```

You can also connect to the running docker image with

```bash
docker exec -it yolov8-fastapi /bin/bash
```

## Helpful documentation

### Fast API

Documentation on how to get stated with FastAPI can be found [here](https://fastapi.tiangolo.com/).


### YOLOv8

https://github.com/ultralytics/ultralytics

## What is next?

There are many areas of improvement that can be made to this project. Some of them are listed below.

- [ ] Add unit test coverage using `from fastapi.testclient import TestClient` [here](https://fastapi.tiangolo.com/tutorial/testing/).
  - [ ] These tests should cover a wide range of expected inputs but also edge cases
    - [ ] Empty image
    - [ ] Image with no objects
    - [ ] Too large image
    - [ ] Different models (yolov8n, yolov8s, yolov8m, yolov8l, yolov8x)
    - [ ] Check that we do not return more than N objects
    - [ ] Check that objects are sorted by confidence
- [ ] Add a frontend to the server that can accept and image and would return the rendered result. Bring it up using docker-compose
- [ ] Collect metrics on the server using Prometheus and Grafana
- [ ] Add api_key authentication
- [ ] Add checks in the middleware for file size to prevent large files from being uploaded
- [ ] Add ability to run on GPU
- [ ] Add a queue system to bundle multiple requests and run them in batches
- [ ] Implement many of the advice from [here](https://github.com/zhanymkanov/fastapi-best-practices).
- [ ] Add option not to include the models inside the docker file. It does make the docker images much larger but does decrease up startup time.
