# Day 5 — Step 0: Setup (about 30 minutes)

Today's tools run a small **Kubernetes** cluster on your laptop and load-test it. Install the four tools, start the cluster, and verify.

---

## 1. Install the tools

| Tool | What it is | Install |
|------|-----------|---------|
| **minikube** | a one-node Kubernetes cluster on your laptop | https://minikube.sigs.k8s.io/docs/start/ |
| **kubectl** | the command-line client for Kubernetes | https://kubernetes.io/docs/tasks/tools/ |
| **helm** | the Kubernetes package manager | https://helm.sh/docs/intro/install/ |
| **k6** | the load-testing tool | https://grafana.com/docs/k6/latest/set-up/install-k6/ |

**On Windows** (our HP EliteBooks) the easiest route is `winget`:

```powershell
winget install Kubernetes.minikube
winget install Kubernetes.kubectl
winget install Helm.Helm
winget install k6.k6
```

(minikube needs Docker Desktop or Hyper-V — both already available from earlier days.)

**On macOS** the easiest route is [Homebrew](https://brew.sh):

```bash
# install Homebrew first if you don't have it:
#   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

brew install minikube       # also pulls in kubectl as a dependency
brew install kubectl        # (explicit, in case it isn't already present)
brew install helm
brew install k6
```

(minikube needs a container/VM driver — **Docker Desktop** is simplest and is already installed from earlier days. On Apple Silicon, `minikube start` auto-selects the Docker driver.)

> All four are also available as plain binaries if Homebrew isn't allowed in your environment — see each tool's official install page in the table above.

Check versions:

```bash
minikube version
kubectl version --client
helm version
k6 version
```

---

## 2. Start the cluster

```bash
minikube start
```

This boots a single-node Kubernetes cluster. Confirm it is healthy:

```bash
kubectl get nodes        # should list one node, STATUS "Ready"
kubectl cluster-info
```

Enable the **metrics-server** add-on (needed later for autoscaling):

```bash
minikube addons enable metrics-server
```

---

## 3. Quick check

```bash
bash day5/00-setup/check_cluster.sh
```

Good result:

```
minikube : OK
kubectl  : OK (node Ready)
helm     : OK
k6       : OK
metrics-server addon: enabled
You are ready for Day 5.
```

---

## Key commands you will use all day

| Action | Command |
|--------|---------|
| List pods | `kubectl get pods` |
| List everything | `kubectl get all` |
| Describe a thing | `kubectl describe pod <name>` |
| Logs of a pod | `kubectl logs <name>` |
| Apply a manifest | `kubectl apply -f file.yaml` |
| Delete a manifest | `kubectl delete -f file.yaml` |
| Open a service URL | `minikube service <name> --url` |
| Port-forward | `kubectl port-forward svc/<name> 8080:80` |

When the cluster is Ready, open **[`../README.md`](../README.md)** and start with Kubernetes.
