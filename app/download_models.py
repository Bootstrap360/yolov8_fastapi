import os

from ultralytics import YOLO

import models


def main():
    for model in models.Models:
        # download the model
        YOLO(os.path.join(models.model_storage_dir, model.name + ".pt"))


if __name__ == "__main__":
    main()
