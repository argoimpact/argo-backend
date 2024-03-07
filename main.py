from fastapi import FastAPI, UploadFile

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.post("/upload-document")
async def upload_document(file: UploadFile):
    return {"filename": file.filename}


@app.post("/summarize")
async def summarize():
    return {"summary": "summarized summary"}
