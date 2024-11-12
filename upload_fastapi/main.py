import uvicorn
import os
import requests
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

# Direktori penyimpanan file
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Endpoint Actix Web untuk menerima metadata
ACTIX_ENDPOINT = "http://localhost:8080/process_metadata"

# Allowed file types
ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/jpg"}

app = FastAPI()

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Form(...),
):
    # Validasi tipe file
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only PNG, JPG, and JPEG files are allowed")

    # Simpan file secara lokal
    try:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            f.write(await file.read())

        # Kirim metadata ke Actix Web
        metadata = {
            "filename": file.filename,
            "content_type": file.content_type,
            "description": description,
        }

        response = requests.post(ACTIX_ENDPOINT, json=metadata)
        response.raise_for_status()  # Memastikan request berhasil

        # Respon dari Actix Web
        actix_response = response.json()

        return JSONResponse(content={
            "message": "File uploaded and metadata sent to Actix",
            "actix_response": actix_response
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail="Error uploading file: " + str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
