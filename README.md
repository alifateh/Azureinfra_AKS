# End-to-End Secure Python Application on Azure AKS

This repository contains the complete configuration and Kubernetes manifests for deploying a secure, cloud-native Python web application on **Azure Kubernetes Service (AKS)**. 

The architecture enforces zero-trust security principles by using **Azure Workload Identity** for passwordless authentication, **Private Endpoints** for secure Azure Key Vault access, and an **Azure Application Gateway (AGIC)** for ingress routing.

---

## 📐 Architecture Overview

![Architecture Diagram](docs/architecture-diagram.png) *(Place your architecture diagram image here)*

### Key Components
- **Azure Kubernetes Service (AKS)**: Hosted cluster running with Azure CNI Overlay networking.
- **Azure Workload Identity**: Passwordless authentication between AKS pods and Azure resources using OpenID Connect (OIDC) federated credentials.
- **Azure Key Vault**: Stores application secrets securely, accessible exclusively over a **Private Endpoint** (`snet_pe`).
- **Azure Application Gateway (AGIC)**: Ingress controller routing external HTTP traffic to the internal Python web service.
- **Azure Container Registry (ACR)**: Private container registry hosting the application image (`acrali.azurecr.io`).

---

## 🛠️ Infrastructure & Naming Standards

| Resource | Name | Details / Subnet |
| :--- | :--- | :--- |
| **Resource Group** | `rg-devops-pmo-uks` | UK West region |
| **Virtual Network** | `vnet_aks_ali` | `10.0.0.0/16` |
| **AKS Subnet** | `snet_aks` | `10.0.0.0/22` |
| **App Gateway Subnet** | `snet_appgw` | `10.0.4.0/24` |
| **Private Endpoint Subnet** | `snet_pe` | `10.0.5.0/24` |
| **AKS Cluster** | `aks_ali` | Managed Kubernetes cluster |
| **Managed Identity** | `id_app_ali` | User-Assigned Managed Identity |
| **Azure Key Vault** | `kv-ITC-ali` | Private Key Vault |
| **Container Registry** | `acrali` | Private ACR |

---

## 🔒 Security & Identity Configuration

### 1. Workload Identity Setup
1. **OIDC & Workload Identity** are enabled on the AKS cluster.
2. A **User-Assigned Managed Identity** (`id_app_ali`) is created with the **Key Vault Secrets User** role on `kv-ITC-ali`.
3. A **Federated Identity Credential** (`fed_cred_ali`) links the Managed Identity to the Kubernetes ServiceAccount:
   - **Issuer**: `https://<region>.oic.prod-aks.azure.com/<tenant-id>/`
   - **Subject**: `system:serviceaccount:dev:app-sa`
   - **Audience**: `api://AzureADTokenExchange`

### 2. Private Endpoint & Networking
- Public access to the Key Vault is restricted.
- A **Private Endpoint** (`vault_EndPoitn_ali`) is attached to `kv-ITC-ali` within `snet_pe` (IP: `10.0.5.4`).
- A **Private DNS Zone** (`privatelink.vaultcore.azure.net`) is linked to `vnet_aks_ali` for internal name resolution.

---

## 🚀 Deployment Steps

### 1. Prerequisites
- Azure CLI authenticated to your subscription.
- `kubectl` connected to the `aks_ali` cluster:
  ```bash
  az aks get-credentials --resource-group rg-devops-pmo-uks --name aks_ali
  ```

### 2. Apply Kubernetes Manifests
Navigate to the repository root and apply the manifests in order:

```bash
# Create Namespace
kubectl create namespace dev

# Apply ServiceAccount with Workload Identity annotation
kubectl apply -f k8s/serviceaccount.yaml

# Deploy Application and Service
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Apply Ingress configuration for App Gateway
kubectl apply -f k8s/ingress.yaml
```

---

## 📁 Repository Structure

```text
.
├── k8s/
│   ├── namespace.yaml
│   ├── serviceaccount.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── ingress.yaml
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
└── README.md
```

---

## 🧪 Verification & Testing

1. **Verify Pod Status**:
   ```bash
   kubectl get pods -n dev
   ```
2. **Check Application Logs (Key Vault Access)**:
   ```bash
   kubectl logs -l app=python-app -n dev
   ```
   *Expected output:*
   ```text
   Loaded: DBPASS
   All Key Vault secrets loaded.
   ```
3. **Local Testing via Port Forwarding**:
   ```bash
   kubectl port-forward pod/<pod-name> 8085:8080 -n dev
   ```

---

## 👤 Author
- **Owner**: Ali
- **Resource Tag**: `Owner: Ali`