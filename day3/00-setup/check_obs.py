"""
Day 3 setup checker: confirms the API and the observability services are up.
Standard library only (urllib), so no extra installs needed to run it.

Usage:
    python day3/00-setup/check_obs.py
"""
import urllib.request


def reachable(url, timeout=4):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return 200 <= r.status < 500   # any non-server-error means it's listening
    except Exception:
        return False


def main():
    targets = [
        ("FastAPI app", "http://localhost:8000/docs", "  [start it first with uvicorn]"),
        ("Prometheus", "http://localhost:9090/-/ready", ""),
        ("Grafana", "http://localhost:3000/api/health", ""),
        ("Loki", "http://localhost:3100/ready", ""),
        ("Jaeger", "http://localhost:16686/", ""),
    ]
    for name, url, note in targets:
        ok = reachable(url)
        port = url.split("//")[1].split("/")[0].split(":")[-1]
        print(f"{name:<14} : {'OK ' if ok else 'DOWN'} (:{port}){'' if ok else note}")


if __name__ == "__main__":
    main()
