# Unoserver

A small FastAPI service for converting office documents with LibreOffice through
`unoserver`.

The container starts `unoserver` in the background, waits until it is ready, and
then serves a simple HTTP API on port `8080`.

## API

- `GET /health` checks whether `unoserver` is ready.
- `POST /convert` converts an uploaded file. The optional `to` query parameter
  controls the output format and defaults to `pdf`.

## Run Locally

Build the image:

```sh
docker build -t unoserver .
```

Start the service:

```sh
docker run --rm -p 8080:8080 unoserver
```

Check health:

```sh
curl http://localhost:8080/health
```

Convert a document to PDF:

```sh
curl -X POST "http://localhost:8080/convert?to=pdf" \
  -F "file=@example.docx" \
  --output example.pdf
```

## Deploy

The repository includes basic Kubernetes manifests:

```sh
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

Before applying them, update the image in `deployment.yaml` to point at your
registry.

## Files

- `server.py` defines the FastAPI application.
- `entrypoint.sh` starts `unoserver` and then `uvicorn`.
- `Dockerfile` builds the LibreOffice-based runtime image.
- `deployment.yaml` and `service.yaml` provide a basic Kubernetes deployment.
