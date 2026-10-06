#!/usr/bin/env bash
# Full run on kind: Vault dev + External Secrets Operator, then wait for the synced Secret.
set -euo pipefail
kind create cluster --name eso-lab
helm repo add external-secrets https://charts.external-secrets.io
helm repo add hashicorp https://helm.releases.hashicorp.com
helm install external-secrets external-secrets/external-secrets --version 0.9.20 -n external-secrets --create-namespace --wait
helm install vault hashicorp/vault --version 0.28.1 -n vault --create-namespace --set server.dev.enabled=true --set server.dev.devRootToken=dev-only-token --wait
kubectl exec -n vault vault-0 -- env VAULT_TOKEN=dev-only-token vault kv put secret/orders-app orders.db.password=from-vault
kubectl create ns orders
kubectl create secret generic vault-token -n orders --from-literal=token=dev-only-token
kubectl apply -f secretstore.yaml
sleep 15
kubectl get secret orders-db -n orders -o jsonpath='{.data.password}' | base64 -d; echo
# Destroy step: kind delete cluster --name eso-lab
