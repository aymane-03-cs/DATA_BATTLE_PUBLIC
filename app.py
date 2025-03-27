from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import ResponseAnalyzer
from vectorstore_utils import get_or_create_vectorstore
from questions_loader import load_questions

app = Flask(__name__)
CORS(app)

# Charger les questions et le vectorstore
questions = load_questions()
vectorstore = get_or_create_vectorstore()
analyzer = ResponseAnalyzer(vectorstore)

@app.route("/questions", methods=["GET"])
def get_questions():
    return jsonify(questions)

@app.route("/submit", methods=["POST"])
def submit_answer():
    data = request.json
    q_type = data.get("type")
    question_text = data.get("question")
    user_answer = data.get("answer")

    if q_type == "qcm":
        # 🔍 Cherche la question dans la base
        matched = next((q for q in questions if q["question"] == question_text), None)
        if not matched:
            return jsonify({"error": "Question introuvable"}), 404

        correct_answer = matched.get("correct_answer", "").strip().lower()
        is_correct = user_answer.strip().lower() == correct_answer
        return jsonify({"correct": is_correct})
    
    elif q_type == "ouverte":
        result = analyzer.analyze_response(question_text, user_answer)
        return jsonify(result)

    return jsonify({"error": "Type de question non valide"}), 400


if __name__ == "__main__":
    app.run(debug=True)
