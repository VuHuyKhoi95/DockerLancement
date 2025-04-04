from weaviate_client import connect_to_weaviate
from vectorstore_setup import get_vectorstore
from retriever_utils import get_dynamic_retriever
from formatting import format_docs
from prompt_chain import build_prompt_chain
import warnings

warnings.simplefilter("ignore", ResourceWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


client = None

try:
    # Connexion
    print("Connexion à Weaviate...")
    client = connect_to_weaviate()
    print("Weaviate prêt :", client.is_ready())

    vectorstore = get_vectorstore(client)
    
    #poser une question
    question = input("\nPose ta question (ou 'exit' pour quitter) : ")

    while question.lower().strip() != "exit":
        retriever = get_dynamic_retriever(vectorstore, question)
        rag_chain = build_prompt_chain(retriever, format_docs)

        # Réponse
        response = rag_chain.invoke(question)

        print("\n---")
        print("Question :", question)
        print("Réponse :\n")
        print(response)
        print("---\n")
        #poser une autre question
        question = input("Pose une autre question (ou 'exit' pour quitter) : ")

except Exception as e:
    print("Une erreur est survenue :", e)

finally:
    if client:
        client.close()
        print("Connexion à Weaviate fermée.")