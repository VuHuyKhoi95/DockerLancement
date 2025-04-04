import json
from pathlib import Path
from langchain_core.documents import Document

def load_json_documents(path: str) -> list[Document]:
    docs_path = Path(path)
    json_files = list(docs_path.glob("*.json"))
    all_docs = []

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            content = data.get("text", "").strip()
            raw_meta = data.get("metadata", {})
            pages = [int(p) for p in raw_meta.get("pages", [])]
            print("pages raw:", raw_meta.get("pages", []), "→ converted:", pages)
            metadata = {
                "title": raw_meta.get("title", "").strip(),
                "authors": raw_meta.get("authors", "").strip(),
                "creationDate": raw_meta.get("creationDate", ""),
                "originalFile": raw_meta.get("originalFile", "").strip(),
                "pages": pages,
                "file_name": file_path.name
            }
            doc = Document(page_content=content, metadata=metadata)
            all_docs.append(doc)

    return all_docs
