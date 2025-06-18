# Certbot Web UI

A simple CherryPy + Bootstrap 5 web interface for issuing and renewing Let's Encrypt certificates using DNS-01 (Cloudflare) challenges.

## Features

- Lightweight Python (CherryPy)
- DNS-01 challenge via Cloudflare
- Dockerized deployment
- Certificate export to `/public-certs`

## Quick Start

```bash
docker-compose up 