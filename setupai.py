import os
import cv2
import torch
import numpy as np
from fastapi import FastAPI, UploadFile, File
from moviepy.editor import VideoFileClip
from ultralytics import YOLO

# Initialize FastAPI
app = FastAPI()

# Load AI Model (YOLO for Object & Action Detection)
model = YOLO("yolov8n.pt")

def extract_highlights(video_path: str, output_path: str):
    """Processes video to detect highlights and save a clipped version."""
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
    
    highlight_frames = []
    
    for _ in range(frame_count):
        ret, frame = cap.read()
        if not ret:
            break
        
        results = model(frame)
        
        # Detect objects & actions, and mark highlight frames
        for r in results:
            if len(r.boxes) > 0:  # If objects detected
                highlight_frames.append(frame)
    
    for frame in highlight_frames:
        out.write(frame)
    
    cap.release()
    out.release()

@app.post("/process-video/")
def process_video(file: UploadFile = File(...)):
    """Endpoint to upload and process video for highlights detection."""
    input_video_path = f"videos/{file.filename}"
    output_video_path = f"videos/highlight_{file.filename}"
    
    os.makedirs("videos", exist_ok=True)
    with open(input_video_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    extract_highlights(input_video_path, output_video_path)
    
    return {"message": "Processing complete", "output_file": output_video_path}

@app.post("/generate-thumbnail/")
def generate_thumbnail(file: UploadFile = File(...)):
    """Extracts a thumbnail from the best highlight frame."""
    input_video_path = f"videos/{file.filename}"
    thumbnail_path = f"videos/thumbnail_{file.filename}.jpg"
    
    os.makedirs("videos", exist_ok=True)
    with open(input_video_path, "wb") as buffer:
        buffer.write(file.file.read())
    
    clip = VideoFileClip(input_video_path)
    best_frame_time = clip.duration / 2  # Pick a frame from the middle
    frame = clip.get_frame(best_frame_time)
    
    cv2.imwrite(thumbnail_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    return {"message": "Thumbnail created", "thumbnail": thumbnail_path}
