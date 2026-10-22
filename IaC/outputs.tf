output "aks_cluster_name" {
  value = azurerm_kubernetes_cluster.aks.name
}

output "key_vault_url" {
  value = azurerm_key_vault.kv.vault_uri
}

output "acr_login_server" {
  value = azurerm_container_registry.acr.login_server
}