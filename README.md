# DockerLancement

## Docker : 

Dockerfile

    FROM python:3.11

    # Créer un utilisateur spécifique pour le conteneur
    RUN useradd -m -u 1000 user
    USER user

    ENV PATH="/home/user/.local/bin:$PATH"

    WORKDIR /app

    # Créer les répertoires d'entrée et de sortie
    RUN mkdir -p /app/input /app/output /app/docs /app/logs

    # Copier le fichier requirements.txt et installer les dépendances
    COPY --chown=user ./requirements.txt requirements.txt
    RUN pip install --no-cache-dir --upgrade -r requirements.txt

    # Copier tous les fichiers dans le conteneur
    COPY --chown=user . /app

    # Exposer les répertoires d'entrée et de sortie comme volumes
    #VOLUME ["/app/input", "/app/output","/app/docs"]

    # Créer un script d'entrée pour exécuter les trois commandes
    RUN printf '#!/bin/bash\npython main_json.py &\npython main_loader.py &\nuvicorn app:app --host 0.0.0.0 --port 7860\n' > /app/start.sh && \
        chmod +x /app/start.sh

    # Utiliser le script comme point d'entrée
    CMD ["/app/start.sh"]


requirements.txt
    langchain
    langchain-community
    langchain-weaviate
    langchain-core
    langchain-huggingface
    langchain_mistralai
    langgraph
    weaviate-client
    python-dotenv
    fastapi
    uvicorn[standard]
    PyMuPDF
    pymupdf4llm

## Creation une image et un conteneur Docker : 

docker build -t pdf_json_weaviate .

docker run -it -v "$(pwd):/home/app" -v "$(pwd)/docs:/app/docs" -p 7860:7860 pdf_json_weaviate

## requirement.txt

pip install -r requirements.txt

Fichier .env contenant les variables : 

WEAVIATE_URL=https://mon-cluster.weaviate.network
WEAVIATE_API_KEY=ma-cle-api-secrete

## Execution par batch les 3 programmes

python main_json.py (charger et traiter les fichiers PDF en JSOn (input : PDF => docs : JSON))
    pdf_processing.py -> Création la structure de la metadonnées et le texte associé
    utils.py -> Nettoyage des données

python main_loader.py (charger les fichiers JSON et mettre dans la base weavaite)
    weaviate_client.py → connecte au cluster Weaviate
    weaviate_collections.py → crée les collections
    weaviate_inserter.py → insère les données dans Weaviate
    
nuvicorn app:app --host 0.0.0.0 --port 7860



## Execution pour le retriever(LLM), une question peut être posée via le terminal, pour quitter : exit

python main_retriever.py

    weaviate_client.py → connecte au cluster Weaviate
    vectorstore_setup.py → récupération du vector store
    retriever_utils.py → pour le type de recherche utilisée ici similarity
    formatting.py → formattage de la source de la réponse
    rag_chain.py → prompt template
