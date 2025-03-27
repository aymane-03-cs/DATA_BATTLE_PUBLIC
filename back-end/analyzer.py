from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate

FEEDBACK_PROMPT = PromptTemplate(
    input_variables=["question", "user_answer", "reference_answer"],
    template="""
You are an expert in European patent law. Your task is to assess student answers to legal exam questions.

Below is an exam response.

## Question
{question}

## User Answer
{user_answer}

## Reference Answer
{reference_answer}

---

### Your task:
Provide a clear and structured feedback in **Markdown** with the following sections:

1. **Legal Concepts** – what's correct or missing?
2. **Procedural Accuracy** – are EPC rules mentioned or correctly applied?
3. **Suggestions for Improvement**
4. **Final Score** – Give a rating from 1 (very poor) to 5 (excellent), and explain briefly why.
Respond only with the feedback. Do not repeat the question or reference answer.
"""
)

class ResponseAnalyzer:
    """
    Classe responsable de l'analyse des réponses utilisateur à des questions ouvertes
    via recherche sémantique + modèle de langage.
    """
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore
        self.llm = ChatOllama(model="tinyllama", temperature=0)
        self.retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    def analyze_response(self, question: str, user_answer: str) -> dict:
        """
        Analyse une réponse ouverte par rapport à une réponse de référence la plus pertinente.

        Args:
            question (str): La question posée
            user_answer (str): La réponse donnée par l'utilisateur

        Returns:
            dict: Résultat contenant feedback, réponse de référence, source, etc.
        """
        try:
            docs = self.retriever.invoke(question)
            if not docs:
                return {"error": "Aucune question correspondante trouvée."}

            # Rassembler plusieurs réponses de référence si disponibles
            ref_answers = "\n\n".join([
                f"- {doc.metadata.get('correct_answer')}\n  (Legal Basis: {doc.metadata.get('legal_basis', 'N/A')})"
                for doc in docs if doc.metadata.get("correct_answer")
            ])

            if not ref_answers:
                return {"error": "Aucune réponse de référence disponible dans les documents."}

            prompt = FEEDBACK_PROMPT.format(
                question=question,
                user_answer=user_answer,
                reference_answer=ref_answers
            )

            response = self.llm.invoke(prompt)
            return {
                "feedback": response.content,
                "reference_answer": ref_answers,
                "source": docs[0].metadata.get("source", "N/A"),
                "page": docs[0].metadata.get("page", "N/A")
            }

        except Exception as e:
            return {"error": f"Échec de l'analyse : {str(e)}"}
