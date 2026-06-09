# 🧠 MindStream — Full-Stack Stream of Consciousness Organizer

An intuitive, distraction-free full-stack web application designed to help users offload unstructured, chaotic thoughts and instantly organize them into actionable tasks and categorized notes. 

Built with a high-performance **FastAPI** backend, **Asynchronous JavaScript**, and powered by **Google Gemini 2.5 Flash** using advanced structured data schemas.

---

## 🚀 Key Features

* **Instant Cognitive Relief:** A clean "Dump & Organize" interface that instantly empties the input field upon submission to relieve immediate mental clutter.
* **AI-Powered Triaging:** Uses Gemini 2.5 Flash to automatically parse and separate a raw stream of consciousness into actionable check-items versus general reference thoughts.
* **Enforced JSON Structuring:** Integrates Pydantic to force the Large Language Model (LLM) to output highly predictable, clean JSON arrays.
* **Interactive Dashboard:** Generates clean, responsive task checklists alongside styled post-it notes for passive concepts.
* **Zero-Refresh UI:** Leverages JavaScript Fetch API to seamlessly handle AI network requests in the background for a fluid user experience.

---

## 🛠️ Tech Stack & Skills Used

* **Backend:** Python, FastAPI, Uvicorn (ASGI Server)
* **AI & Data Engineering:** Google GenAI SDK (Gemini 2.5 Flash), Pydantic (Structured Output Enforcing)
* **Frontend:** HTML5, CSS3 (Grid & Flexbox Layouts), Asynchronous JavaScript (Fetch API)
* **Security & Environment:** Dotenv (`.env`), Git Version Control (`.gitignore`)

---

## ⚙️ How It Works (Under the Hood)

1. The user inputs a raw, messy block of text into the frontend UI.
2. JavaScript intercepts the submission and sends an asynchronous `POST` request containing the text to the FastAPI `/dump` endpoint.
3. The Python backend invokes the Gemini API, passing a custom system instruction along with a strict **Pydantic data validation model** (`SortedBrainDump`).
4. Gemini extracts the core components of the text and formats them flawlessly into `tasks` and `notes` keys.
5. The frontend reads the returned JSON data and dynamically renders clean, interactive checkboxes and stylized note cards.