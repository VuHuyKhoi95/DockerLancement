def format_docs(docs):
    formatted = []
    for doc in docs:
        file_name = doc.metadata.get("file_name", "Inconnu")
        authors = doc.metadata.get("authors", "Auteur inconnu")
        content = doc.page_content
        formatted.append(f"Auteur : {authors}\nFichier : {file_name}\n\n{content}")
    
    sources = [f"- {doc.metadata.get('file_name', 'Inconnu')}" for doc in docs]
    return "\n\n---\n\n".join(formatted) + "\n\nSources:\n" + "\n".join(sources)
