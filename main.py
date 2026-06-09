from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

# 1. Load the hidden secrets from your local .env file
load_dotenv()

app = FastAPI()
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=CURRENT_DIR), name="static")

# Define the exact JSON structure we want the AI to return
class SortedBrainDump(BaseModel):
    tasks: list[str] = Field(description="Actionable things the user needs to do/complete.")
    notes: list[str] = Field(description="Creative ideas, thoughts, references, or general diary entries that aren't strict tasks.")

class DumpRequest(BaseModel):
    text: str

# 2. Safely initialize the Gemini client using the hidden key
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_path = os.path.join(CURRENT_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return f.read()

@app.post("/dump")
async def process_dump(request: DumpRequest):
    try:
        # Call Gemini and force it to fill out our Pydantic data structure
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Analyze this chaotic ADHD brain dump and sort it neatly: {request.text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SortedBrainDump,
                system_instruction="You are an expert ADHD organizational assistant. Strip away conversational fluff and extract clean, bite-sized tasks and notes."
            ),
        )
        
        import json
        return json.loads(response.text)
        
    except Exception as e:
        return {"error": str(e), "tasks": [], "notes": ["An error occurred while calling the AI engine."]}