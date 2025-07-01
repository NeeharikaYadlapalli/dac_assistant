import os

from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()
BUCKET_NAME = os.environ.get("SERVER_BUCKET_NAME")

def list_gcs_modules( prefix=None):
    """
    Lists all files (modules) in a GCS bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        prefix (str, optional): A prefix to filter files. Defaults to None.

    Returns:
        list: A list of file names in the bucket.
    """
    # Initialize the GCS client
    client = storage.Client()

    # Get the bucket
    bucket = client.bucket(BUCKET_NAME)

    # List blobs in the bucket
    blobs = bucket.list_blobs(prefix=prefix)

    # Collect file names
    file_names = [blob.name for blob in blobs]

    return file_names


def delete_server(server_name):
    """
    Deletes a server from the GCS bucket.

    Args:
        server_name (str): The name of the server to delete.
    """
    try:
        # Initialize the GCS client
        client = storage.Client()

        # Get the bucket
        bucket = client.bucket(BUCKET_NAME)

        # Delete the server file
        blob = bucket.blob(server_name)
        blob.delete()
        return True
    except Exception as e:
        print(f"Error deleting server: {e}")
        return False
