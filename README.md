cat > README.md <<'EOF'
# FastAPI + PostgreSQL (Docker Compose)

Минимальный микросервис (FastAPI) с PostgreSQL. Данные хранятся в volume, конфигурация через переменные окружения. Есть два способа запуска: локальная сборка и запуск из Docker Hub.

- **GitHub:** https://github.com/apoluskin61-bot/apoluskin61-bot-my-microservice
- **Docker Hub:** `alexlll1451/my-microservice:latest`
- **Сервис-доки (Swagger):** http://localhost:8000/docs

---

## Стек
- FastAPI + Uvicorn
- PostgreSQL 16 (alpine)
- Docker / Docker Compose
- Персистентность: volume `pgdata`

## Структура


my-microservice/
├─ app/
│ ├─ app.py
│ ├─ db.py
│ ├─ requirements.txt
│ └─ init.py
├─ Dockerfile
├─ docker-compose.yml # локальная сборка (build: .)
├─ compose.hub.yml # запуск из Docker Hub (image:)
├─ .dockerignore
├─ .env # локальные секреты (НЕ коммитить)
└─ .env.example # шаблон без секрета


## Переменные окружения
Файл `.env` (локально, не коммитить):


POSTGRES_DB=appdb
POSTGRES_USER=appuser
POSTGRES_PASSWORD=strong_local_password


---

## Запуск (локальная сборка)
```bash
docker compose up --build -d

curl http://localhost:8000/ping
# {"message":"pong"}

curl http://localhost:8000/status
# {"service":"ok","db_host":"db","db":"appdb"}

curl -X POST http://localhost:8000/data \
  -H "Content-Type: application/json" \
  -d '{"content":"hello from compose"}'

curl http://localhost:8000/data

docker compose down
docker compose up -d
curl http://localhost:8000/data   # записи должны сохраниться
docker compose -f compose.hub.yml pull
docker compose -f compose.hub.yml up -d

docker login -u alexlll1451
docker build -t alexlll1451/my-microservice:latest .
docker push alexlll1451/my-microservice:latest

docker login -u alexlll1451
docker build -t alexlll1451/my-microservice:latest .
docker push alexlll1451/my-microservice:latest

docker compose down -v
docker system prune -af
docker volume prune -f
docker compose up --build -d

docker compose -f compose.hub.yml down -v
docker image rm alexlll1451/my-microservice:latest || true
docker system prune -af && docker volume prune -f
docker compose -f compose.hub.yml pull
docker compose -f compose.hub.yml up -d

Траблшутинг

/data даёт 500 — БД ещё не поднялась. Ждите db (healthy) или перезапустите app.

pull access denied — образ не запушен/приватный. Проверь docker push и логин.

В VM нужен доступ из Windows-хоста — включите NAT Port Forwarding 8000→8000 или используйте Bridged.

connection refused — проверьте docker compose ps, логи docker compose logs -f app db.


После вставки файл создастся. Проверь и запушь:

```bash
ls -l README.md
git add README.md
git commit -m "Add README with run, verify, Hub and troubleshooting"
git push


