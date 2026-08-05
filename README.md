# DATA_BATTLE_PUBLIC — RAG web app for patent exam training

A Retrieval-Augmented Generation (RAG) web application for training and evaluating answers to patent exam questions. Learners can answer multiple-choice (QCM) and open-ended questions; open-ended answers are evaluated by retrieving relevant reference material from a semantic vectorstore and producing structured feedback with a local LLM.

## Key features
- Automatic evaluation of multiple-choice (QCM) answers.
- Open-ended answer analysis using semantic retrieval + LLM feedback.
- Retrieval powered by FAISS + HuggingFace embeddings.
- Local LLM integration via Ollama (example: tinyllama).
- Lightweight Vue 3 + Vite frontend with Markdown rendering.

## Stack
- Languages: Python (backend), Vue (frontend), CSS/HTML
- Backend: Flask
- Retrieval / RAG: LangChain + FAISS, HuggingFace embeddings (`all-MiniLM-L6-v2`)
- LLM runtime: Ollama via langchain_ollama (example model: `tinyllama`)
- Frontend: Vue 3 + Vite, marked for Markdown rendering

## Project layout
```
backend/               Flask API, retrieval + analyzer, question data
  app.py               Flask routes (GET /questions, POST /submit)
  analyzer.py          RAG + LLM prompt + feedback generation
  vectorstore_utils.py create/load FAISS vectorstore and retriever
  questions_loader.py  Loads questions from backend/questions/questions.json
  requirements.txt
  questions/           JSON source files (questions.json)
  analyzer_test.py     unit test(s) for analyzer functionality

frontend/              Vue 3 + Vite app for quiz UI
  package.json
  src/
    App.vue            main app UI
    main.js
    style.css
  index.html
  vite.config.js
README.md               top-level README (this file)
```

## How it fits together
- The frontend fetches questions from the backend (`GET /questions`), renders QCM and open-ended questions, and sends answers to the backend (`POST /submit`).
- For QCM questions the backend compares the submitted answer to the stored `correct_answer` and returns a boolean result.
- For open-ended questions the backend uses the vectorstore retriever to find relevant reference passages, builds a prompt (see `backend/analyzer.py`), and calls the local LLM via Ollama to produce structured feedback.

## Quick start : Backend
1. Requirements: Python 3.8+
2. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Prepare vectorstore and embeddings:
   - `backend/vectorstore_utils.py` includes logic to create/load a FAISS vectorstore.
   - Ensure access to the embeddings model (example: `all-MiniLM-L6-v2`) and that `backend/questions/questions.json` exists.
4. Run the server:
   ```bash
   python3 backend/app.py
   ```
   The Flask app runs by default at http://127.0.0.1:5000.

Notes:
- Ollama must be installed and running for analyzer LLM calls to work. `analyzer.py` currently uses `ChatOllama(model="tinyllama", temperature=0)` — adapt as needed.
- Questions are loaded from `backend/questions/questions.json` via `questions_loader.py`.

## Quick start — Frontend
1. Requirements: Node.js (16+/18+ recommended)
2. From the repository root:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
3. Vite dev server will start (usually at http://localhost:5173). The frontend expects the backend API to be reachable (CORS is enabled in the Flask app).

## API examples
- Get questions:
  ```bash
  curl http://localhost:5000/questions
  ```
- Submit a QCM answer:
  ```bash
  curl -X POST http://localhost:5000/submit -H "Content-Type: application/json" \
    -d '{"type":"qcm","question":"<question text>","answer":"A"}'
  ```
  Response: {"correct": true|false}
- Submit an open-ended answer:
  ```bash
  curl -X POST http://localhost:5000/submit -H "Content-Type: application/json" \
    -d '{"type":"ouverte","question":"<question text>","answer":"<user answer text>"}'
  ```
  Response: JSON containing `feedback`, `reference_answer`, `source`, and other metadata (or an `error` key).

## Configuration & important notes
- Analyzer: uses LangChain + Ollama. If you don't run Ollama locally, modify `backend/analyzer.py` to use another LLM provider or mock the LLM for testing.
- Embeddings: the project references HuggingFace embeddings — ensure network access or local model availability as needed.
- Vectorstore: `backend/vectorstore_utils.py` handles the FAISS store; rebuild the store if you change the reference corpus.
- Tests: run or extend `backend/analyzer_test.py` to validate analyzer behavior.

## Where to edit content
- Add or edit questions and reference answers: `backend/questions/questions.json`.
- Modify analysis prompt and scoring: `backend/analyzer.py` (constant `FEEDBACK_PROMPT`).
- Change vectorstore/retriever parameters: `backend/vectorstore_utils.py` and `backend/analyzer.py`.

## Troubleshooting
- If open-ended analysis fails:
  - Verify Ollama is running and accessible.
  - Verify embeddings can be computed (network/credentials).
  - Verify the vectorstore exists and contains documents.
- Frontend issues: ensure both frontend dev server and backend Flask server are running and that frontend points to the correct backend origin.



