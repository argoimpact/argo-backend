# Argo backend

Running a uvicorn server with a redis in memory db for caching

# building

```
python -m venv venv
source venv/bin/activate
```

```
docker compose up --build
```

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
