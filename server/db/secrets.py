

from google.cloud.secretmanager import SecretManagerServiceClient

PROJECT_ID = 'delta-timer-368701'

client = SecretManagerServiceClient()


def get_secret_value(secret_name: str) -> str:
    request_name = f'projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest'
    response = client.access_secret_version(request={'name': request_name})
    return response.payload.data.decode('UTF-8')
