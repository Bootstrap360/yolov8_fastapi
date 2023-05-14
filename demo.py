# A test script that calls the fast API with an image
import base64
import os

import requests
import app
import app.models
from app.models import Models, Result


def main():
    # img_path = "/tmp/zidane.jpg"
    # if not os.path.exists(img_path):
    #     # download image from 'https://ultralytics.com/images/zidane.jpg'
    #     with open(img_path, "wb") as f:
    #         f.write(r.content)

    url = "https://ultralytics.com/images/zidane.jpg"
    r = requests.get(url, allow_redirects=True)
    url = "http://localhost:8061/predict"

    # Perform object detection

    for model in Models:
        image = r.content
        files = {"file": image}
        # print(model.name)

        params = {"render": True, "model_name": model.name, "image_size": 640}
        response = requests.post(url=url, files=files, params=params)
        os.makedirs("./results", exist_ok=True)

        if response.ok:
            result = response.json()
            result = Result(**result)
            print(result)
            render = result.render
            if render:
                render = base64.b64decode(render)
                path = f"./results/{model.name}.jpg"
                with open(path, "wb") as f:
                    f.write(render)
        else:
            print(repr(response), response.content, response.reason)


if __name__ == "__main__":
    main()
