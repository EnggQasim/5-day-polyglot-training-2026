# Kubernetes — Step 2: Containerize the API

Before Kubernetes can run our API, we package it as a **container image**. The app is a small stateless FastAPI service in [`app/main.py`](app/main.py) (in-memory leaderboard + a `/work` CPU-burn endpoint for load tests).

---

## The Dockerfile

[`app/Dockerfile`](app/Dockerfile) describes how to build the image:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

- **`FROM`** — start from a small Python base image.
- **`COPY requirements.txt` then `RUN pip install`** — install deps in their own layer so rebuilds are fast (Docker caches it until requirements change).
- **`CMD`** — what runs when the container starts: uvicorn on `0.0.0.0:8000` (must be `0.0.0.0`, not `localhost`, so it's reachable from outside the container).

---

## Build the image *into* minikube

minikube has its **own** Docker, separate from your laptop's. The simplest way to make the image available to the cluster is to build it with minikube directly:

```bash
minikube image build -t pixelquest-api:1.0 day5/kubernetes/app
```

- `-t pixelquest-api:1.0` names and tags the image.
- The last argument is the build context (the folder with the Dockerfile).

Confirm it's there:

```bash
minikube image ls | grep pixelquest
```

> **Why this matters:** our `deployment.yaml` uses `image: pixelquest-api:1.0` with `imagePullPolicy: IfNotPresent`, so Kubernetes uses this **locally built** image instead of trying to pull it from an internet registry — important in a closed environment.

---

## (Optional) test the image directly

You can run it once outside Kubernetes to confirm it works:

```bash
minikube image build -t pixelquest-api:1.0 day5/kubernetes/app
# or test on your laptop's Docker:
#   docker build -t pixelquest-api:1.0 day5/kubernetes/app
#   docker run -p 8000:8000 pixelquest-api:1.0
#   curl localhost:8000/health   ->  {"status":"ok","pod":"..."}
```

Now we have an image the cluster can run. Next we declare a Deployment and Service.

➡️ Next: **[03-deployments-and-services.md](03-deployments-and-services.md)**

---

## ⭐ Must-learn from this topic

- **Dockerfile** — `FROM` / `COPY` / `RUN` / `CMD`; layer caching for deps.
- **Bind to `0.0.0.0`** — so the container is reachable from outside.
- **`minikube image build`** — make a local image the cluster can use.
- **`imagePullPolicy: IfNotPresent`** — use the local image (closed-network friendly).

### 📚 Official docs
- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/) — image instructions.
- [minikube — handling images](https://minikube.sigs.k8s.io/docs/handbook/pushing/) — local images.
- [Images in Kubernetes](https://kubernetes.io/docs/concepts/containers/images/) — pull policies.
