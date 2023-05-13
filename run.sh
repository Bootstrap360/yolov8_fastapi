#!/bin/bash

set -e
set -x

source ./.env/bin/activate

cd src
uvicorn main:app --host 0.0.0.0 --port 8061 --reload