# Argo backend

Running a uvicorn server with a redis in memory db for caching

## Local development

`app/congif.py` uses pydantic BaseSettings to load environment variables. for local development, create a .env file and put relevant environment variables in there. DON'T COMMIT THIS FILE

# building

We're using `poetry` for dependency management and building.

(prereq, install pyenv and select the right python version)

1. Install poetry to your system.
2. Poetry install

## testing

```
pytest
```

## login to ghcr

```
echo $'YOUR_PERSONAL_ACCESS_TOKEN' | docker login ghcr.io -u YOUR_GITHUB_USERNAME --password-stdin
```

### housekeeping

updating requirements:

```
pip review --auto
pip freeze > requirements.txt
# add/commit/push
```

# docs

http://localhost:8000/docs
