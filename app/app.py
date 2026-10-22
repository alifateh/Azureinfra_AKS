import os
from flask import Flask
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

app = Flask(__name__)

# گرفتن متغیرهای محیطی
KEY_VAULT_URL = os.environ.get("KEY_VAULT_URL")
SECRET_NAME = os.environ.get("SECRET_NAME", "dbpass")

@app.route("/")
def home():
    try:
        # احراز هویت با استفاده از Workload Identity و DefaultAzureCredential
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KEY_VAULT_URL, credential=credential)
        
        # خواندن سکرت از Key Vault
        retrieved_secret = client.get_secret(SECRET_NAME)
        
        return f"<h1>Azure AKS & Workload Identity Success!</h1><p>Successfully retrieved secret '{SECRET_NAME}' from Key Vault.</p>"
    except Exception as e:
        return f"<h1>Error connecting to Key Vault</h1><p>{str(e)}</p>", 500

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)