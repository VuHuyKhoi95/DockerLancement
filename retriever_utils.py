
def get_dynamic_retriever(vectorstore, question: str):
    print("Recherche vectorielle standard sans filtre.")
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )

