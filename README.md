# Enterprise Bot — DevOps Take-Home

## Overview

This repository contains a containerized HTTP service, a Helm chart, a local Kubernetes setup script, and a Kubernetes debugging lab.

## Prerequisites

Install Docker, kind, kubectl, and Helm. Ensure Docker is running before deployment.

## Run the application

From the repository root, run:

```bash
chmod +x setup.sh
./setup.sh
```

The script creates or reuses the kind cluster named `demo`, installs the NGINX Ingress controller, builds and loads the application image, and deploys the Helm release in namespace `demo`.

## Verify the deployment

```bash
kubectl get deployments,pods,services,ingress -n demo
kubectl get pods -n demo
kubectl rollout status deployment/demo -n demo --timeout=180s
```

Check the actual service name using `kubectl get services -n demo`. Then port-forward using that name:

```bash
kubectl port-forward -n demo svc/demo 8080:8080
```

In another terminal, test the endpoints:

```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/
```

## Resource sizing rationale

The chart defaults to two replicas, CPU requests of 100m and memory requests of 64Mi, with limits of 500m CPU and 128Mi memory. These are modest starting values for a small demonstration service. Requests support Kubernetes scheduling, while limits constrain container resource usage. Production values should be validated through load testing and monitoring.

## Limitations and skipped work

This setup is intended for local development, not production. Production DNS and TLS, load testing, CI/CD security scanning, and full production monitoring have not been implemented. In the debugging lab, the reporter workload and its pod-count reporting check remain unresolved; see `lab/FINDINGS.md`.

## Production-readiness improvements

- Add automated CI tests, image vulnerability scanning, and dependency checks.
- Pin and verify image digests and publish signed build provenance.
- Configure production DNS, TLS, and secrets management.
- Add monitoring, alerting, dashboards, and centralized logs.
- Review resource sizing under load; consider autoscaling and PodDisruptionBudgets.
- Apply least-privilege RBAC and network policies.
- Fix the remaining reporter issue and rerun all lab checks before declaring the lab fully passing.

## AI-use disclosure

I used ChatGPT to help reason about debugging output and organize documentation and findings. I ran commands and checked their outputs myself, applied fixes based on observed behavior, and documented the unresolved reporter issue rather than claiming it was fixed.