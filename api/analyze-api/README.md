# PlayTherapy_Backend/analyze-api

## Install Env

```bash
pip install poetry
```

## Install Dependency

```bash
cd api/analyze-api
poetry install --sync
```

## Run
```bash
cd api/analyze-api
poetry run uvicorn main:app --reload --app-dir analyze
```

## Test

```bash
cd api/analyze-api
poetry run python -m unittest discover -s tests
```

## Docs
```bash
http://localhost:8000/docs
```