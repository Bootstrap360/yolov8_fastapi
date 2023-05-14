from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class BoundingBox(BaseModel):
    xmin: float
    ymin: float
    xmax: float
    ymax: float


class Stats(BaseModel):
    speed: dict
    model_name: str
    inference_size: List[int]
    image_size: List[int]


class Prediction(BaseModel):
    name: str
    confidence: float
    box: BoundingBox


class Result(BaseModel):
    render: Optional[str]
    predictions: List[Prediction]
    stats: Stats


model_storage_dir = "/tmp"


class Models(str, Enum):
    yolov8n = "yolov8n"
    yolov8s = "yolov8s"
    yolov8m = "yolov8m"
    yolov8l = "yolov8l"
    yolov8x = "yolov8x"


class UnprocessableError(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Example Error Message."},
        }


class OkResponse(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "Example Error Message."},
        }
