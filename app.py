import json
import os
from pathlib import Path

import numpy as np
import io
from fastapi import FastAPI, File, Form, UploadFile
from loguru import logger
from model import load_predictor
import matplotlib.pyplot as plt

app = FastAPI()
version = "0.0.1"
model = None

MODEL_STORE = "model_store"


@app.on_event("startup")
async def startup_event():
    if not Path(MODEL_STORE).is_dir():
        os.makedirs(MODEL_STORE)
    global model
    model = load_predictor("model_store/wrist-detection/1.0/detection-model-created-on-2020-07-24.pth")
    logger.info(f"model loaded")


@app.get("/")
async def root():
    return {"message": f"Running version: {version}"}


def read_image(npz):
    buf = io.BytesIO(npz)
    npzfile = np.load(buf)
    return npzfile["arr_0"]


@app.post("/predictions")
async def predictions(file: UploadFile = File(...)):
    print(type(file), file.content_type)
    image = read_image(await file.read())
    print(image.shape)
    plt.imsave("/tmp/a.png", image, cmap="gray")
    outputs = model(image)
    out = outputs["instances"].to("cpu")
    bboxes = out.pred_boxes.tensor.numpy()
    classes = out.pred_classes.numpy()
    return {"bboxes": bboxes, "classes": classes}

