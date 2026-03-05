# PromptHelp

A minimal prompt optimization app that uses FastAPI + Ollama to refine user prompts before submitting them to AI models.

## Setup

1. Install dependencies:
```bash
pip install fastapi uvicorn jinja2 httpx
```

2. Make sure Ollama is running:
```bash
ollama serve
```

3. Pull a model (e.g., llama3):
```bash
ollama pull llama3
```

4. Run the app:
```bash
uvicorn main:app --reload
```

5. Open http://localhost:8000 in your browser

## How it works

- Enter your raw prompt in the text area
- Select or enter the Ollama model name
- Click "Optimize Prompt"
- Copy the optimized prompt and use it with any AI model
