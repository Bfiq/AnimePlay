from azure.storage.blob import BlobServiceClient
import uuid
from decouple import config

class AzureBlobService:
    def __init__(self):
        self.connection_string = config('AZURE_STORAGE_CONNECTION_STRING')
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_name = config('CONTAINER_NAME')
        self.container_client = self.blob_service_client.get_container_client(self.container_name)

    def upload_image(self, image):
        image_name = f"{uuid.uuid4()}-{image.name}"
        blob_client = self.container_client.get_blob_client(image_name)
        blob_client.upload_blob(image, overwrite=True)
        print(blob_client.url)
        return blob_client.url