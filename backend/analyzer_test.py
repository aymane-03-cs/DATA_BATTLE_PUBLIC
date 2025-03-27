import sys
import os
import time

#  Permet d'importer les fichiers du dossier parent
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analyzer import ResponseAnalyzer
from vectorstore_utils import get_or_create_vectorstore

#  Chargement du vectorstore
print(" Loading vectorstore...")
vectorstore = get_or_create_vectorstore()
analyzer = ResponseAnalyzer(vectorstore)

#  Question + réponse utilisateur
question = "What are the requirements for patentability of an invention under the EPC?"
user_answer = "The invention must be new and useful."

#  Timer de début
print(" Running analysis...")
start_time = time.time()

# Analyse de la réponse
result = analyzer.analyze_response(question, user_answer)

#  Timer de fin
end_time = time.time()
elapsed = round(end_time - start_time, 2)

#  Résultat
print(f"\n Execution time: {elapsed} seconds")

if "error" in result:
    print(" Error:", result["error"])
else:
    print(" Reference answer:\n", result["reference_answer"])
    print("\n Feedback:\n", result["feedback"])
    print(f"\n Source: {result['source']} (Page {result['page']})")


