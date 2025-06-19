# Certbot Web UI

A simple CherryPy + Bootstrap 5 web interface for issuing and renewing Let's Encrypt certificates using DNS-01 (Cloudflare) challenges.

## Features

- Lightweight Python (CherryPy)
- DNS-01 challenge via Cloudflare
- Dockerized deployment
- Certificate export to `/public-certs`

## Quick Start
Download the docker-compose.yml in your project folder

Enter your cloudflare token in ./secrets/cloudflare.ini
You can create the folder and the file within the project directory

run
docker-compose up -d
