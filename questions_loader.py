import json
import os

PATH = os.path.join("questions", "questions.json")

def load_questions():
    """
    Charge les questions du fichier JSON et les transforme dans un format exploitable par le frontend.
    
    Retour :
        List[Dict] : Liste de questions (QCM ou ouvertes)
    """
    file_path = PATH
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    questions = []
    for item in raw_data:
        q_type = "qcm" if "options" in item else "ouverte"
        q = {
            "id": item.get("number"),
            "type": q_type,
            "question": item.get("question"),
            "options": item.get("options") if q_type == "qcm" else None,
            "correct_answer": item.get("correct_answer"),
            "legal_basis": item.get("legal_basis", None)
        }
        questions.append(q)

    return questions
