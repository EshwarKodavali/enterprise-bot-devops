
#!/usr/bin/env bash
set -Eeuo pipefail

CLUSTER_NAME="demo"
NAMESPACE="demo"
RELEASE_NAME="demo"
IMAGE_NAME="enterprise-bot:1.0.0"

echo "==> Checking kind cluster: ${CLUSTER_NAME}"

if kind get clusters | grep -qx "${CLUSTER_NAME}"; then
  echo "==> Reusing existing kind cluster: ${CLUSTER_NAME}"
else
  echo "==> Creating kind cluster: ${CLUSTER_NAME}"
  kind create cluster --name "${CLUSTER_NAME}"
fi

echo "==> Selecting the expected Kubernetes context"
kubectl config use-context "kind-${CLUSTER_NAME}"

echo "==> Current Kubernetes context:"
kubectl config current-context

echo "==> Installing or updating NGINX Ingress controller"
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

echo "==> Waiting for NGINX Ingress controller"
kubectl rollout status deployment/ingress-nginx-controller \
  --namespace ingress-nginx \
  --timeout=180s

echo "==> Building application image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" ./service

echo "==> Loading application image into kind"
kind load docker-image "${IMAGE_NAME}" --name "${CLUSTER_NAME}"

echo "==> Creating namespace if needed"
kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -

echo "==> Installing or upgrading Helm release: ${RELEASE_NAME}"
helm upgrade --install "${RELEASE_NAME}" ./chart \
  --namespace "${NAMESPACE}" \
  --set image.repository=enterprise-bot \
  --set image.tag=1.0.0 \
  --wait \
  --timeout 180s

echo "==> Deployment completed"
kubectl get deployments,pods,services,ingress -n "${NAMESPACE}"
