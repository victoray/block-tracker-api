celery: bin/start-stunnel celery -A worker.celery_app worker -E --loglevel=info
web: bin/start-stunnel uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}