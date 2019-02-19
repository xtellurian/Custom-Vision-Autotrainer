import os
import uuid
from azure.storage.blob import BlockBlobService

class BlobClient:
    blob_service: BlockBlobService
    container_names = ['train', 'test', 'holdout']

    def __init__(self, blob_service: BlockBlobService):
        """
        :param block_blob_service: A block blob service
        :type: azure.storage.blob.BlockBlobService
        """
        self.blob_service = blob_service

    def initialise_containers(self):
        """
        Creates the containers required in the storage account
        """
        for name in self.container_names:
            self.blob_service.create_container(name)

    def add_data_from_path(self, container_name: str, file_path: str, parent: str = None, labels: [str] = []):
        """
        Creates a new file in blob storage
        :param container_name: One of self.container_names
        :type: str
        :param file_path: Path to the file to upload
        :type: str
        :param parent: Directory in blob storage. None will create a new directory
        :type: str
        :param labels: List of labels for the file
        :type: [str]
        """
        filename=os.path.basename(file_path)
        if parent is None:
            parent = str(uuid.uuid4())
        if not parent.endswith('/'):
            parent = parent + '/'

        self.blob_service.create_blob_from_path(container_name, parent + filename, file_path )
        text=''
        for label in labels:
            text+=label + '\n'
        print(text)
        self.blob_service.create_blob_from_text(container_name, parent + filename + '.labels', text)
