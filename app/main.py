import base64
import os
from enum import Enum
from io import BytesIO
from typing import Literal, Optional

import cv2
import numpy as np
import ultralytics
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import RedirectResponse
from PIL import Image
from ultralytics import YOLO

from .models import BoundingBox, Models, Prediction, Result, Stats, UnprocessableError

ultralytics.checks()

app = FastAPI()
model_storage_dir = "/tmp"

models = {
    model.name: YOLO(os.path.join(model_storage_dir, model.name + ".pt"))
    for model in Models
}


@app.get("/")
def root():
    # redirect to docs
    response = RedirectResponse(url="/docs")
    return response


@app.post(
    "/predict",
    responses={
        status.HTTP_200_OK: {
            "description": "Ok Response",
        },
        422: {
            "model": UnprocessableError,
            "description": "Could not process the image",
        },
    },
)
async def predict(
    file: UploadFile = File(...),
    inference_size: int = 640,
    render: bool = True,
    model_name: Models = Models.yolov8s,
):
    bytes = BytesIO(await file.read())

    if not bytes.getvalue() or len(bytes.getvalue()) == 0:
        raise HTTPException(status_code=422, detail="File is empty")

    image = Image.open(bytes)

    model = models.get(model_name.name)
    results = model(image, imgsz=inference_size)

    # will only get one result
    result = results[0]

    # https://docs.ultralytics.com/reference/yolo/engine/model/?h=ultralytics.yolo.engine.results.results

    # Process the results
    boxes = result.boxes
    names = result.names

    predictions = []

    stats = Stats(
        speed=result.speed,
        model_name=model_name.name,
        inference_size=[inference_size, inference_size],
        image_size=image.size,
    )

    for box in boxes:
        cls = int(box.cls[0])
        conf = float(box.conf[0])
        xyxy = box.xyxy[0]
        cls_name = names[cls]
        xmin, ymin, xmax, ymax = xyxy

        bounding_box = BoundingBox(
            xmin=xmin,
            ymin=ymin,
            xmax=xmax,
            ymax=ymax,
        )

        prediction = Prediction(name=cls_name, confidence=conf, box=bounding_box)
        predictions.append(prediction)

    rtn_result = Result(predictions=predictions, stats=stats)

    if render:
        plot_img: np.ndarray = result.plot()
        # convert the plot_img to base64
        plot_img = Image.fromarray(plot_img)
        plot_img: np.ndarray = cv2.cvtColor(np.array(plot_img), cv2.COLOR_BGR2RGB)

        buffered = BytesIO()
        plot_img = Image.fromarray(plot_img)
        plot_img.save(buffered, format="JPEG")
        plot_img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        rtn_result.render = plot_img_b64

    # reset the file pointer
    bytes.seek(0)

    return rtn_result
