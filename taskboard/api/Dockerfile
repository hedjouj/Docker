FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system --gid 10001 appuser \
 && useradd --system --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin appuser

# Dépendances avant le code : la couche pip reste en cache tant que requirements.txt ne change pas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code en lecture seule pour l'utilisateur applicatif (propriétaire root)
COPY app.py .

# ARG placé après pip install : changer de version n'invalide pas le cache des dépendances
ARG APP_VERSION=1.0.0
LABEL org.opencontainers.image.title="taskboard-api" \
      org.opencontainers.image.description="API REST TaskBoard (Flask + gunicorn)" \
      org.opencontainers.image.version="${APP_VERSION}"

USER 10001:10001
EXPOSE 5000

# Python est déjà présent : pas besoin d'installer curl
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --start-interval=2s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/api/health', timeout=4)"]

CMD ["gunicorn", "-b", "0.0.0.0:5000", "--access-logfile", "-", "app:app"]
