from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def build_prompt_chain(retriever, format_docs):
    prompt_template = """
    Tu es un assistant pour les tâches de réponse aux questions.
    Utilise les éléments de contexte suivants pour répondre à la question.
    Si tu ne connais pas la réponse, dis simplement que tu ne sais pas. Utilise trois phrases maximum et garde la réponse concise.

    Question: {question}

    Context: {context}

    Reponse:
    (Si possible, cite tes sources en fin de réponse)
    """
    
    prompt = ChatPromptTemplate.from_messages([("system", prompt_template)])
    llm = ChatMistralAI(model="mistral-large-latest")

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )