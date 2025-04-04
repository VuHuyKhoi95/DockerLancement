from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_huggingface import HuggingFaceEmbeddings

def get_vectorstore(client):
    embeddings = HuggingFaceEmbeddings()

    vectorstore = WeaviateVectorStore(
        client=client,
        index_name="Article",
        text_key="text",
        attributes=["file_name", "authors"],
        embedding=embeddings
    )
    return vectorstore
