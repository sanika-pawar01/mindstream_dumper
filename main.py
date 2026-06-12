from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import json
import traceback
from sqlmodel import Session, select

# Database imports
from database import create_db_and_tables, get_session
from models import MindDump

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Mount static files
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=CURRENT_DIR), name="static")

# Models
class SortedBrainDump(BaseModel):
    tasks: list[str] = Field(description="Actionable things the user needs to do/complete.")
    notes: list[str] = Field(description="Creative ideas, thoughts, references, or general diary entries that aren't strict tasks.")

class DumpRequest(BaseModel):
    text: str

# Gemini Client Setup
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("CRITICAL: GEMINI_API_KEY is not set in environment variables.")

client = genai.Client(api_key=API_KEY)

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    index_path = os.path.join(CURRENT_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/dump")
async def process_dump(request: DumpRequest, session: Session = Depends(get_session)):
    try:
        if not API_KEY:
            raise ValueError("API Key is missing. Please check Render environment variables.")

        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"Analyze this chaotic ADHD brain dump and sort it neatly: {request.text}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=SortedBrainDump,
                system_instruction="You are an expert ADHD organizational assistant. Strip away conversational fluff and extract clean, bite-sized tasks and notes."
            ),
        )
        
        result_data = json.loads(response.text)
        
        # Save to Database
        new_dump = MindDump(
            content=request.text, 
            tasks=", ".join(result_data["tasks"]), 
            notes=", ".join(result_data["notes"])
        )
        session.add(new_dump)
        session.commit()
        
        return result_data
        
    except Exception as e:
        # Print full error to logs for debugging
        print("DEBUG ERROR:", traceback.format_exc())
        # Return error to UI for immediate feedback
        return {
            "tasks": [], 
            "notes": [f"Error: {str(e)} - Check Render Logs for details."]
        }

@app.get("/history", response_class=HTMLResponse)
async def get_history(request: Request, session: Session = Depends(get_session)):
    dumps = session.exec(select(MindDump)).all()
    return templates.TemplateResponse(
        request=request, 
        name="history.html", 
        context={"dumps": dumps}
    )