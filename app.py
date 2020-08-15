import json
import os
from pathlib import Path
from shutil import copyfile, copyfileobj
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()
version = "0.0.1"

MODEL_STORE = "model_store"

@app.on_event("startup")
async def startup_event():
    if not Path(MODEL_STORE).is_dir():
        os.makedirs(MODEL_STORE)


@app.get("/")
async def root():
    return {"message": f"Running version: {version}"}


@app.post("/models")
async def register(file: UploadFile = File(...), meta: str = Form(...)):
    meta_data = json.loads(meta)
    foldername = meta_data.get("name", "no_name_given") + "_" + meta_data.get("version", "no_version_given")
    os.makedirs(Path(MODEL_STORE) / Path(foldername), exist_ok=True)
    with (Path(MODEL_STORE) / Path(foldername) / file.filename).open("wb") as buffer:
        copyfileobj(file.file, buffer)
    return {"filename": file.filename, "meta": meta_data}
