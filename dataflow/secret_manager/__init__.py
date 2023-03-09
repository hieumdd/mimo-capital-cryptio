from google.auth import default
from google.cloud import secretmanager


def get_secret(secret_id: str) -> str:
    _, project_id = default()
    client = secretmanager.SecretManagerServiceClient()

    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    response = client.access_secret_version(request={"name": name})

    return response.payload.data.decode("UTF-8")
