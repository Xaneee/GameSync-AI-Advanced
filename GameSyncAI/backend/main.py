# Main entry point for FastAPI backend
from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def read_root():
    return {"message": "GameSync AI Backend is running successfully!"} 