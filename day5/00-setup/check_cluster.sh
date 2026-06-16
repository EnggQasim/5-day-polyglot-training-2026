#!/usr/bin/env bash
# Day 5 setup checker: confirms the cluster tools are installed and the
# minikube cluster is up with metrics-server enabled.

ok() { printf "%-8s : %s\n" "$1" "$2"; }

command -v minikube >/dev/null && ok "minikube" "OK" || ok "minikube" "MISSING"
if kubectl get nodes 2>/dev/null | grep -q " Ready"; then
  ok "kubectl" "OK (node Ready)"
else
  ok "kubectl" "cluster not Ready (run: minikube start)"
fi
command -v helm >/dev/null && ok "helm" "OK" || ok "helm" "MISSING"
command -v k6 >/dev/null && ok "k6" "OK" || ok "k6" "MISSING"

if minikube addons list 2>/dev/null | grep metrics-server | grep -q enabled; then
  echo "metrics-server addon: enabled"
else
  echo "metrics-server addon: NOT enabled (run: minikube addons enable metrics-server)"
fi

echo "If all show OK, you are ready for Day 5."
