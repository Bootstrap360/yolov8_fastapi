FROM python:3.8
# specify image name

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
RUN cd /code; python -c "import app; print(app.__file__)"; python /code/app/download_models.py

# Start the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8061"]
