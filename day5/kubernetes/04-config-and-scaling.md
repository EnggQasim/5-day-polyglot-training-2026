# Kubernetes — Step 4: Config and scaling

Two everyday operations: feed configuration into Pods (**ConfigMap/Secret**) and change how many copies run (**scaling**).

---

## ConfigMaps (and Secrets)

You should not bake settings into the image — different environments need different values. A **ConfigMap** holds non-secret config; a **Secret** holds sensitive values (passwords, tokens). Both get injected into Pods as environment variables or files.

[`manifests/configmap.yaml`](manifests/configmap.yaml):

```yaml
apiVersion: v1
kind: ConfigMap
metadata: { name: pixelquest-config }
data:
  GREETING: "Welcome to Pixel Quest on Kubernetes"
  ENVIRONMENT: "training"
```

Apply it and inject the values into the Deployment's container (add under the container spec):

```bash
kubectl apply -f day5/kubernetes/manifests/configmap.yaml
```

```yaml
          envFrom:
            - configMapRef:
                name: pixelquest-config
```

Now every Pod has `GREETING` and `ENVIRONMENT` as env vars. A **Secret** is identical but created with `kubectl create secret` and shown masked.

> Rule of thumb: **config in ConfigMaps, sensitive data in Secrets, never in the image.**

---

## Scaling: more copies

### Manual scaling

Change the number of replicas on the fly:

```bash
kubectl scale deployment pixelquest --replicas=5
kubectl get pods            # watch it go to 5 pods
```

Kubernetes starts 3 more Pods; the Service automatically begins load-balancing across all 5. Scale back with `--replicas=2`.

Or edit `replicas:` in `deployment.yaml` and re-`apply` — same result, but now it's in version control (the declarative way, which is preferred).

### Rolling updates

When you change the image (say `pixelquest-api:1.1`) and re-apply, Kubernetes does a **rolling update**: it starts new Pods, waits for them to pass the readiness probe, then removes old ones — **no downtime**. If the new version is broken, roll back:

```bash
kubectl rollout status deployment pixelquest    # watch a rollout
kubectl rollout undo deployment pixelquest       # go back to the previous version
```

---

## Watch it work

```bash
kubectl get pods -w        # -w = watch live as pods are added/removed
```

Run `kubectl scale ... --replicas=5` in another terminal and watch new Pods appear and become Ready.

**Manual scaling is fine when you know the load. For traffic that spikes unpredictably, you want the cluster to scale itself — that's the autoscaler (after the lab).**

➡️ Next: the lab — **[05-lab-deploy-pixelquest.md](05-lab-deploy-pixelquest.md)**

---

## ⭐ Must-learn from this topic

- **ConfigMap / Secret** — config & secrets injected as env/files; never in the image.
- **Manual scaling** — `kubectl scale` or edit `replicas` and re-apply.
- **Rolling updates & rollback** — `rollout status` / `rollout undo`, no downtime.
- **Declarative > imperative** — keep desired state in version-controlled YAML.

### 📚 Official docs
- [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) and [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/).
- [Scaling a Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#scaling-a-deployment).
- [Rolling updates](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/).
