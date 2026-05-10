import os
import httpx
from fastapi import FastAPI, Response, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="PiTTS Frontend Gateway")

class TTSRequest(BaseModel):
    text: str
    voice: str = "en_US-lessac-medium"
    speed: float = 1.0

@app.get("/")
async def index():
    # Serve the static HTML page
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/api/tts")
async def proxy_tts(req: TTSRequest):
    """
    Proxy the request to the Knative Piper backend.
    This hides the backend URL and handles CORS naturally.
    """
    async with httpx.AsyncClient() as client:
        try:
            # We set a slightly longer timeout to account for Knative Cold Starts
            # The very first request might take 3-5s if the pod was scaled to zero!
            print(f"DEBUG: Proxying request to KEDA Interceptor for host: tts-backend.internal")
            response = await client.post(
                f"http://keda-add-ons-http-interceptor-proxy.keda.svc.cluster.local:8080/generate", 
                json=req.model_dump(),
                headers={"Host": "tts-backend.internal"},
                timeout=60.0
            )
            response.raise_for_status()
            
            # Return the raw audio bytes directly to the browser
            return Response(
                content=response.content, 
                media_type="audio/wav"
            )
        except httpx.ReadTimeout:
            print("DEBUG: ReadTimeout from backend (Cold Start)")
            raise HTTPException(status_code=504, detail="Backend took too long to start (Cold Start Timeout)")
        except Exception as e:
            print(f"DEBUG: Unexpected error in proxy: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
