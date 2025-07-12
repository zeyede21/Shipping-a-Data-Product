## Setup

```bash
git clone <repo>
cd project
cp .env.example .env
```

## Run with Docker Compose

```bash
docker-compose up --build
```

## Run Scripts

```bash
docker-compose exec app python src/db_loader.py
```
