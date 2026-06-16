# Helm — Step 2: Chart anatomy

Our chart lives in [`chart/`](chart/). A Helm chart is just a folder with a fixed layout:

```
chart/
├── Chart.yaml            # name, version, appVersion
├── values.yaml           # default settings (the knobs)
└── templates/
    ├── deployment.yaml   # templated Deployment
    └── service.yaml      # templated Service
```

---

## Chart.yaml — the chart's identity

[`chart/Chart.yaml`](chart/Chart.yaml):

```yaml
apiVersion: v2
name: pixelquest
version: 0.1.0       # the CHART version
appVersion: "1.0"    # the APP/image version it deploys
```

`version` is the chart itself; `appVersion` tracks the app it ships. Bump `version` when you change the chart, `appVersion` when the app image changes.

---

## values.yaml — the knobs

[`chart/values.yaml`](chart/values.yaml):

```yaml
replicaCount: 2
image:
  repository: pixelquest-api
  tag: "1.0"
  pullPolicy: IfNotPresent
service:
  type: ClusterIP
  port: 80
  targetPort: 8000
resources:
  requests: { cpu: 100m, memory: 128Mi }
  limits:   { cpu: 250m, memory: 256Mi }
```

These are the **defaults**. Anyone installing the chart can override them without touching the templates.

---

## Templates — YAML with placeholders

[`chart/templates/deployment.yaml`](chart/templates/deployment.yaml) (excerpt):

```yaml
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: api
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          imagePullPolicy: {{ .Values.image.pullPolicy }}
          resources:
{{ toYaml .Values.resources | indent 12 }}
```

- **`{{ .Values.replicaCount }}`** pulls `replicaCount` from `values.yaml`.
- **`{{ .Release.Name }}`** (used in the metadata name) is the release name you give at install — so two installs don't collide.
- **`{{ toYaml .Values.resources | indent 12 }}`** drops the whole `resources` block in, indented correctly — a common Helm idiom.

## See the rendered YAML before installing

`helm template` fills the placeholders and prints the final YAML **without** touching the cluster — perfect for checking:

```bash
helm template my-test day5/helm/chart
```

You'll see the same Deployment/Service as the raw manifests, but generated from values. Change a value and re-run to see it update.

➡️ Next: the lab — **[03-lab-package-and-install.md](03-lab-package-and-install.md)**

---

## ⭐ Must-learn from this topic

- **Chart layout** — `Chart.yaml`, `values.yaml`, `templates/`.
- **`version` vs `appVersion`** — chart version vs app/image version.
- **Templating** — `{{ .Values.* }}`, `{{ .Release.Name }}`, `toYaml | indent`.
- **`helm template`** — render to YAML to check before installing.

### 📚 Official docs
- [Charts](https://helm.sh/docs/topics/charts/) — structure & metadata.
- [Chart template guide](https://helm.sh/docs/chart_template_guide/) — templating language.
- [Values](https://helm.sh/docs/chart_template_guide/values_files/) — defaults & overrides.
