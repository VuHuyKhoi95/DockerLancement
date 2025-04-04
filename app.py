from fastapi import FastAPI
from pydantic import BaseModel
from chatbot import get_answer

# Création de l'app FastAPI
app = FastAPI()

# Schéma de la requête
class ChatRequest(BaseModel):
    question: str

# Schéma de la réponse
class ChatResponse(BaseModel):
    answer: str

@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l'API du chatbot!"}

# Endpoint principal du chatbot
"""
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    user_question = request.question

    # Ici, tu connecteras ton chatbot (LangChain, RAG, etc.)
    # Pour l'instant, on retourne une réponse factice
    fake_response = f"Tu m'as demandé : '{user_question}' — mais je suis un bot fictif^^"

    return ChatResponse(answer=fake_response)
"""
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    user_question = request.question
    answer = get_answer(user_question)
    return ChatResponse(answer=answer)

