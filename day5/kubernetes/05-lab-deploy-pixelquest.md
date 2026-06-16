# Kubernetes — Step 5: LAB (deploy Pixel Quest end to end)

Do the whole flow yourself: build the image, deploy, expose, reach it, scale, and self-heal. All manifests are in [`manifests/`](manifests/).

---

## Step 1 — build the image into minikube

```bash
minikube image build -t pixelquest-api:1.0 day5/kubernetes/app
minikube image ls | grep pixelquest
```

## Step 2 — deploy and expose

```bash
kubectl apply -f day5/kubernetes/manifests/deployment.yaml
kubectl apply -f day5/kubernetes/manifests/service.yaml
kubectl get all          # see the deployment, 2 pods, and the service
```

Wait until both pods are `Running` and `READY 1/1`:

```bash
kubectl get pods -w
```

## Step 3 — reach the API

```bash
kubectl port-forward svc/pixelquest 8080:80
# another terminal:
curl localhost:8080/health
curl localhost:8080/players      # run a few times; the "pod" field alternates
```

The changing `pod` value proves the Service is **load-balancing** across the two replicas.

## Step 4 — scale

```bash
kubectl scale deployment pixelquest --replicas=5
kubectl get pods         # now 5 pods
# hit /players again -> responses come from more pods
```

## Step 5 — watch it self-heal

Delete a Pod and watch Kubernetes replace it to keep the replica count:

```bash
kubectl get pods
kubectl delete pod <one-pod-name>
kubectl get pods -w      # a new pod appears within seconds
```

You never asked for a new Pod — the Deployment's controller reconciled back to the desired count. That's the core Kubernetes promise.

---

## What you achieved

- Built a local image and ran it on Kubernetes via a **Deployment**.
- Exposed it with a load-balancing **Service**.
- **Scaled** replicas and saw the Service spread traffic.
- Watched Kubernetes **self-heal** a deleted Pod.

### Deliverable for this track
Commit the manifests. In your notes: *What is the difference between a Pod, a Deployment, and a Service? What happened (step by step) when you deleted a Pod?*

➡️ Next: **[../helm/01-why-helm.md](../helm/01-why-helm.md)**

---

## ⭐ Must-learn from this topic

- **The full flow** — build image → deploy → expose → reach → scale.
- **Load balancing** — the `pod` field changes across replicas.
- **Self-healing** — delete a Pod, the controller replaces it.
- **Declarative apply** — everything reproducible from YAML.

### 📚 Official docs
- [Deploy an app](https://kubernetes.io/docs/tutorials/kubernetes-basics/deploy-app/deploy-intro/) — the basics tutorial.
- [Port forwarding](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/).
- [kubectl cheatsheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/).
