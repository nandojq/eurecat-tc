# NBA Analytics Pipeline

## Eurecat Technical Challenge

**Fernando Jorge Ques**

This repository contains an NBA Analytics Pipeline designed for the Eurecat Technical Challenge. The pipeline ingests data from the NBA API, processes it, and stores it in a normalized database for analytical purposes. A FastAPI-based API is also included for querying and interacting with the data.

## Launch Pipeline Logic

To run the pipeline logic and start the data processing, use the following command:

```bash
python ./src/main.py
```

This will trigger the pipeline, fetching data from the NBA API and processing it according to the logic defined in the script.

## API

To build and run the FastAPI API container for serving the data:

1. **Build the Docker image:**

```bash
docker build -t analytics-api .\src\api\
```

2. **Run the Docker container with a mounted volume:**

```bash
docker run -p 8000:8000 -v C:\Users\Fer\Desktop\Code\eurecat-tc\db\sqlite-db:/app/sqlite-db.db analytics-api
```

This will start the FastAPI service, and you can access the API at `http://localhost:8000`.

### API Endpoints:
- `/players`: To fetch all player data
- `/player/{id}`: To get specific player data by ID
- `/alldata`: To get the whole data table

