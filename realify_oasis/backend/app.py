from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.posture_analysis import analyze_posture
import cv2
import numpy as np
import tempfile
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze_video(file: UploadFile = File(...)):
    # Save video file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        shutil.copyfileobj(file.file, temp_video)
        temp_video_path = temp_video.name

    # Open the video using OpenCV
    cap = cv2.VideoCapture(temp_video_path)

    # Analyze the video
    result = analyze_posture(cap)

    # Cleanup
    cap.release()
    os.remove(temp_video_path)

    return {"result": result}
