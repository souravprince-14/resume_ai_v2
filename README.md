# Resume Matcher AI

This Streamlit app analyzes an uploaded resume against a pasted job description using a local Ollama model (preferred) or the Ollama CLI as a fallback. Optionally, if you have LangChain + Ollama integrations installed, the app will use `OllamaLLM` via LangChain.

## Prerequisites
- Python 3.10+ (3.11/3.12 recommended)
- Ollama installed and daemon running. Ensure the model you want is available locally, e.g. `ollama:latest`.
- A virtual environment (recommended)

## Setup
1. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Confirm Ollama is running and the model exists:

```powershell
ollama ls
```

If the daemon is not running, start it according to your Ollama installation instructions.

## Run the app

```powershell
streamlit run app.py
```

## Notes
- The app tries to use `langchain_core` + `langchain_ollama` if installed. If those packages aren't available or the LangChain call fails, it falls back to the `ollama` CLI (`ollama generate` or `ollama run`).
- Use the `Model name` input in the UI to choose a model (default: `ollama:latest`).
- Enable `Show debug logs` to display error details returned from the Ollama CLI or LangChain runtime.

If you want, I can pin specific versions for `langchain-core` and `langchain-ollama` that I've tested, or add a small integration test harness to validate Ollama connectivity automatically.