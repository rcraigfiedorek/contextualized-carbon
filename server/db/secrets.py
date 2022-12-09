import os
import warnings

from google.auth.exceptions import DefaultCredentialsError
from google.cloud.secretmanager import SecretManagerServiceClient

PROJECT_ID = "delta-timer-368701"


def get_google_secret_value(secret_name: str) -> str:
    client = SecretManagerServiceClient()
    request_name = f"projects/{PROJECT_ID}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": request_name})
    return response.payload.data.decode("UTF-8")


def get_db_password() -> str:
    if "EMISSIONS_DB_PASSWORD" in os.environ:
        return os.getenv("EMISSIONS_DB_PASSWORD")
    if "EMISSIONS_DB_PASSWORD_FILE" in os.environ:
        with open(os.getenv("EMISSIONS_DB_PASSWORD_FILE"), "r") as f:
            return f.read()
    try:
        return get_google_secret_value("EMISSIONS_DB_PASSWORD")
    except DefaultCredentialsError:
        warnings.warn(
            "Could not determine database password. Please set using one of:\n1)"
            " EMISSIONS_DB_PASSWORD environment variable\n2)"
            " EMISSIONS_DB_PASSWORD_FILE environment variable\n3) By granting access"
            f' to GCP Secret Manager for the "{PROJECT_ID}" project\n'
        )
        return None
