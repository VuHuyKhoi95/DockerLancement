# chatbot.py

from weaviate_client import connect_to_weaviate
from vectorstore_setup import get_vectorstore
from retriever_utils import get_dynamic_retriever
from formatting import format_docs
from prompt_chain import build_prompt_chain

def get_answer(question: str) -> str:
    client = None
    try:
        client = connect_to_weaviate()
        vectorstore = get_vectorstore(client)
        retriever = get_dynamic_retriever(vectorstore, question)
        rag_chain = build_prompt_chain(retriever, format_docs)

        response = rag_chain.invoke(question)
        return str(response)

    except Exception as e:
        return f"Erreur : {e}"

    finally:
        if client:
            client.close()
