from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
import os

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Serve static files only if the directory exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


class PromptRequest:
    def __init__(self, prompt: str, model: str = "llama3"):
        self.prompt = prompt
        self.model = model


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/optimize")
async def optimize_prompt(request: Request):
    data = await request.json()
    raw_prompt = data.get("prompt")
    model_name = data.get("model", "llama3")

    if not raw_prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    # 1. Ask Ollama to optimize the prompt
    optimize_instruction = f"""
You are an AI prompt engineer. Below is a user's raw prompt. Return only a refined, clear, and effective version of the prompt that will help an AI model generate better responses. Do not add explanations or comments.

User prompt:
{raw_prompt}
"""

    ollama_payload = {
        "model": model_name,
        "prompt": optimize_instruction,
        "stream": False,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json=ollama_payload,
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            optimized = data.get("response", "").strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calling Ollama: {str(e)}")

    return JSONResponse({"optimized": optimized})
