# Pelican Pricing

Pelican Pricing, a quote service. It stores price quotes with an expiry date and serves them over a small JSON API.

## Run locally

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

```sh
curl localhost:8000/health
curl -X POST localhost:8000/quotes -H 'content-type: application/json' \
  -d '{"product":"starter","amount_cents":4900,"currency":"EUR","expires_at":"2027-01-31T00:00:00Z"}'
curl localhost:8000/quotes
```

## Routes

| Method | Path      | Description                                                                       |
| ------ | --------- | --------------------------------------------------------------------------------- |
| GET    | `/health` | `{"ok": true}`                                                                    |
| GET    | `/quotes` | all quotes, oldest first                                                          |
| POST   | `/quotes` | create one: `product`, `amount_cents`, `currency` (ISO 4217), `expires_at` (ISO 8601) |

## Environment

| Variable       | Default                       | Purpose                                                                 |
| -------------- | ----------------------------- | ----------------------------------------------------------------------- |
| `DATABASE_URL` | `sqlite:///./pelican.sqlite3` | SQLAlchemy URL. `postgres://` and `postgresql://` URLs are accepted.    |
| `PORT`         | `8000`                        | port uvicorn listens on                                                 |

With `DATABASE_URL` unset, the service, the migrations and the cleanup script all use the SQLite file
`pelican.sqlite3` in the working directory (ignored by git). Set a Postgres URL for anything shared.

## Migrations

Schema changes live in `alembic/`. Run `alembic upgrade head` against the target database before a new
version takes traffic; the service does not create tables on its own. New migrations:
`alembic revision --autogenerate -m "describe the change"`.

## Cleanup

`python scripts/cleanup.py` deletes quotes whose `expires_at` is in the past and prints how many it removed.
Run it from the repository root with the same `DATABASE_URL` as the service.
