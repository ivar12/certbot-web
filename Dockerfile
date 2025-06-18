FROM python:3.13.5-slim-bookworm

RUN apt-get update && apt-get install -y \
    certbot \
    python3-certbot-dns-cloudflare \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY certbot_web.py .
COPY templates/ ./templates

RUN pip install cherrypy jinja2

EXPOSE 8080

CMD ["python", "certbot_web.py"]