FROM python:3.11

# Créer un utilisateur spécifique pour le conteneur
RUN useradd -m -u 1000 user
USER user
#ENV PATH="/home/user/.local/bin:$PATH"
ENV PATH="/home/user/.local/bin:$PATH"

RUN echo "L'environnement est : $PATH"
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
