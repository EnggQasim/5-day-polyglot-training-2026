# Helm — Step 3: LAB (package & install)

Install the Pixel Quest chart, override a value, upgrade, and roll back — the real Helm lifecycle. Chart: [`chart/`](chart/).

**Prerequisite:** the image is built into minikube (`minikube image build -t pixelquest-api:1.0 day5/kubernetes/app`). If you still have the raw-manifest deployment from the Kubernetes lab, remove it first so names don't clash:
```bash
kubectl delete -f day5/kubernetes/manifests/ 2>/dev/null
```

---

## Step 1 — check the rendered YAML

```bash
helm template pq day5/helm/chart | head -40
```

This prints the final Deployment/Service Helm will create — no cluster changes yet.

## Step 2 — install

```bash
helm install pq day5/helm/chart
helm list                 # shows release "pq"
kubectl get all           # the deployment, 2 pods, and service Helm created
```

`pq` is the **release name**. Reach the app the same way as before:

```bash
kubectl port-forward svc/pq-pixelquest 8080:80
curl localhost:8080/players
```

## Step 3 — override a value (no template edits)

Scale to 4 replicas just by overriding `replicaCount`:

```bash
helm upgrade pq day5/helm/chart --set replicaCount=4
kubectl get pods          # now 4 pods
```

That's the Helm win: change behaviour with `--set` (or a values file), not by editing YAML.

## Step 4 — upgrade & roll back

Every `install`/`upgrade` is a **revision**. View and roll back:

```bash
helm history pq           # list revisions
helm rollback pq 1        # back to the first revision (replicaCount=2)
kubectl get pods          # back to 2 pods
```

## Step 5 — uninstall

```bash
helm uninstall pq         # removes everything the chart created
```

---

## What you achieved

- Rendered, **installed**, and managed an app as a single Helm **release**.
- Changed config with **`--set`** instead of editing manifests.
- Used **`helm upgrade` / `history` / `rollback`** — the real release lifecycle.

### Deliverable for this track
Commit the chart. In your notes: *What does Helm give you over raw `kubectl apply`? How would you deploy this same chart to "staging" with 1 replica and "prod" with 6?* (Hint: per-environment values.)

➡️ Next: **[../autoscale/01-hpa.md](../autoscale/01-hpa.md)**

---

## ⭐ Must-learn from this topic

- **Release lifecycle** — `install` → `upgrade` → `rollback` → `uninstall`.
- **`--set` overrides** — change values without editing files.
- **Revisions & history** — every change is versioned; roll back instantly.
- **Render first** — `helm template` to preview.

### 📚 Official docs
- [helm install](https://helm.sh/docs/helm/helm_install/) / [helm upgrade](https://helm.sh/docs/helm/helm_upgrade/).
- [helm rollback](https://helm.sh/docs/helm/helm_rollback/) — revisions.
- [Values & overrides](https://helm.sh/docs/chart_template_guide/values_files/) — `--set` / `-f`.
