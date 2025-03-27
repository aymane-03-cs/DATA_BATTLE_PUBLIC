
---

##  `backend/README.md`

```md
#  Patent Exam Backend (Flask + LangChain)

This backend powers the patent training app. It serves questions and evaluates open-ended answers using semantic retrieval and LLM feedback.

---

##  Tech Stack

-  Flask API
-  LangChain + FAISS for semantic search
-  HuggingFace Embeddings (`all-MiniLM-L6-v2`)
-  Ollama for running local LLMs like `tinyllama` or `mistral`, make sure to adapt it in "Analyzer.py"

---
##  Installation
```bash

pip install -r requirements.txt

---

## Lunching the server

```bash

python3 app.py
