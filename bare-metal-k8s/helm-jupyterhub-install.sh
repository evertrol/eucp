#! /bin/bash

helm repo add jupyterhub https://jupyterhub.github.io/helm-chart/
helm repo update

RELEASE=jhub
NAMESPACE=jhub

# 0.8.2 JupyterHub Helm chart = JupyterHub 0.9.6, and requires Kubernetes 1.11+, Helm 2.11.0+
helm upgrade --install $RELEASE jupyterhub/jupyterhub \
  --namespace $NAMESPACE  \
  --version=0.8.2 \
  --values jupyterhub-config.yaml

kubectl get service --namespace jhub

# To update values:
#helm upgrade -f updated-values.yml $RELEASE jupyterhub/jupyterhub

# Cleaning up:
#helm delete --purge $RELEASE
#kubectl delete namespace $NAMESPACE
