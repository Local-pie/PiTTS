import os
import subprocess
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI(title="Piper TTS API")

class TTSRequest(BaseModel):
    text: str
    voice: str = "en_US-lessac-medium"
    speed: float = 1.0

@app.post("/generate")
async def generate_audio(req: TTSRequest):
    # In a real Docker container, models would be downloaded to /models
    # e.g. /models/en_US-lessac-medium.onnx
    model_path = f"/models/{req.voice}.onnx"
    
    # Ensure tmp directory exists
    os.makedirs("/tmp", exist_ok=True)
    output_file = f"/tmp/{uuid.uuid4()}.wav"
    
    command = [
        "piper", 
        "--model", model_path, 
        "--length_scale", str(1/req.speed), 
        "--output_file", output_file
    ]
    
    # We pass the text via stdin
    process = subprocess.Popen(
        command, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    # We don't want to block the event loop for too long in a real prod app,
    # but piper is very fast. For high concurrency, consider asyncio.subprocess
    stdout, stderr = process.communicate(input=req.text.encode('utf-8'))
    
    if process.returncode != 0:
        raise HTTPException(
            status_code=500, 
            detail=f"Piper generation failed: {stderr.decode()}"
        )
        
    return FileResponse(
        output_file, 
        media_type="audio/wav", 
        filename="tts.wav"
    )

@app.get("/health")
async def health_check():
    # Knative uses this to know the pod is ready
    return {"status": "ok"}
