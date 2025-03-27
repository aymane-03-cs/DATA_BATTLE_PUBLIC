import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from questions_loader import load_questions

def get_or_create_vectorstore(persist_path="vectorstore"):
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    if os.path.exists(persist_path):
        print("📁 Chargement de l'index FAISS existant...")
        return FAISS.load_local(
            persist_path, 
            embedding_model, 
            allow_dangerous_deserialization=True
        )

    print("🆕 Création d’un nouvel index FAISS...")
    questions = load_questions()
    documents = []

    for idx, q in enumerate(questions):
        if q.get("type") == "ouverte":
            print(f"[DEBUG] Document ajouté : {q['question'][:60]}...")
            documents.append(Document(
                page_content=q["question"],
                metadata={
                    "correct_answer": q.get("correct_answer", "Réponse de référence indisponible"),
                    "source": "questions.json",
                    "page": idx + 1
                }
            ))

    print(f"Nombre de documents à indexer : {len(documents)}")

    if not documents:
        raise ValueError("Aucune question ouverte à indexer dans FAISS.")

    print("🧠 Test de génération des embeddings...")
    test_embeddings = [embedding_model.embed_query(doc.page_content) for doc in documents]
    print(f"[DEBUG] Exemple d'embedding : {test_embeddings[0][:5]}")

    vectorstore = FAISS.from_documents(
        documents, 
        embedding_model, 
    )

    vectorstore.save_local(persist_path)
    return vectorstore
