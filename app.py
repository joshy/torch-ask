from fastapi import FastAPI, File, UploadFile, Form
import json

app = FastAPI()
version = "0.0.1"


@app.get("/")
async def root():
  return {"message": f"Running version: {version}"}


@app.post("/models")
async def register(file: UploadFile = File(...), meta: str = Form(...)):
    meta_data = json.loads(meta)
    return {"filename": file.filename, "meta": meta_data}