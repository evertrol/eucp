#! /bin/bash

# Install Helm from https://github.com/helm/helm/releases
# For macOS, this also works if you are using Homebrew:
brew install kubernetes-helm

#Using Helm version 2.14.1
#Kubectl version: 1.15.0 client / 1.15.1 server
kubectl version

#Set up a service account for Tiller:
kubectl --namespace kube-system create serviceaccount tiller

#Set RBAC permissions:
kubectl create clusterrolebinding tiller --clusterrole cluster-admin --serviceaccount=kube-system:tiller
#Check with:
kubectl get clusterrolebinding

#Initialize Helm and set up Tiller in the cluster:
helm init --service-account tiller --wait

# See the Tiller pod running:
kubectl get pod -n kube-system -l name=tiller

# Secure Helm & Tiller:
kubectl patch deployment tiller-deploy --namespace=kube-system --type=json --patch='[{"op": "add", "path": "/spec/template/spec/containers/0/command", "value": ["/tiller", "--listen=localhost:44134"]}]'
# patch doesn't have a --wait flag
sleep 30

helm version
