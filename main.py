from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import uuid, shutil
from depth_processing import process_depth_video

app = FastAPI()

UPLOAD_DIR = Path("/tmp/uploads")
OUTPUT_DIR = Path("/tmp/outputs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=OUTPUT_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def frontend():
    return Path("frontend/index.html").read_text(encoding="utf-8")

@app.post("/upload")
async def upload_video(file: UploadFile):
    uid = str(uuid.uuid4())
    input_path = UPLOAD_DIR / f"{uid}.mp4"
    output_path = OUTPUT_DIR / f"{uid}_depth.mp4"

    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    process_depth_video(str(input_path), str(output_path))

    return {
        "status": "done",
        "download_url": f"/static/{uid}_depth.mp4"
    }