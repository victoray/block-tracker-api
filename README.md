# Block Tracker Api

Block tracker is a blockchain tracking application that helps users keep track of their cryptocurrencies.
The app supports almost all the existing cryptocurrencies and shows the latest
price for each cryptocurrency.

## Requirements
- Redis
- Python >= 3.8
- Google Cloud

## Environment Variables
The following environment variables need to be set for the server to run locally,
A working version of the backend runs here https://blocktracker.herokuapp.com/
```shell
CMC_KEY=
MAILGUN_API_KEY=
REDIS_URL=
GOOGLE_CREDENTIALS=
```

## Getting Started

Run celery background worker
```shell
celery -A worker.celery_app worker -E --loglevel=info
```
Start the server in a new tab
```shell
celery -A worker.celery_app worker -E --loglevel=info
```




