FROM nginxinc/nginx-unprivileged:1.27-alpine

# L'image tourne déjà sous l'utilisateur nginx (UID 101) et écoute sur 8080.
# Les fichiers copiés restent propriété de root : nginx peut les lire, pas les modifier.
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html

ARG APP_VERSION=1.0.0
LABEL org.opencontainers.image.title="taskboard-front" \
      org.opencontainers.image.description="Front TaskBoard (nginx non-root, reverse proxy /api/)" \
      org.opencontainers.image.version="${APP_VERSION}"

EXPOSE 8080

# wget (busybox) est présent dans l'image alpine. 127.0.0.1 plutôt que localhost : nginx n'écoute qu'en IPv4.
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --start-interval=2s --retries=3 \
  CMD ["wget", "-q", "-O", "/dev/null", "http://127.0.0.1:8080/healthz"]
