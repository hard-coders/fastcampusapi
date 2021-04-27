from tempfile import NamedTemporaryFile
from typing import IO

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


async def save_file(file: IO):
    with NamedTemporaryFile("wb", delete=False) as tempfile:
        tempfile.write(file.read())
        return tempfile.name


@app.post("/file/size")
async def get_filesize(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/file/info")
async def get_file_info(file: UploadFile = File(...)):
    return {
        "content_type": file.content_type,
        "filename": file.filename
    }


@app.post("/file/store")
async def store_file(file: UploadFile = File(...)):
    path = await save_file(file.file)
    return {"filepath": path}
