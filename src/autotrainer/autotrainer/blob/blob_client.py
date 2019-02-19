import os
import uuid
from datetime import datetime, timedelta
from azure.storage.blob import ( 
    BlockBlobService,
    BlobPermissions
)

# Helper methods
def join_parent_and_file_name(parent:str, file_name: str):
    if not parent.endswith('/'):
        parent = parent + '/'
    return parent + file_name

def join_parent_and_file_name_labels(parent:str, file_name: str):
    if not parent.endswith('/'):
        parent = parent + '/'
    return parent + file_name + '.labels'

# model class

class LabelledBlob:
    download_url: str
    labels: [str]

    def __init__(self, download_url: str, labels: [str]):
        self.download_url = download_url
        self.labels = labels


# main blob client class

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
        full_name = join_parent_and_file_name(parent, filename)
        labels_full_name = join_parent_and_file_name_labels(parent, filename)
        self.blob_service.create_blob_from_path(container_name, full_name, file_path )
        text=''
        for label in labels:
            text+=label + '\n'
        
        self.blob_service.create_blob_from_text(container_name, labels_full_name, text.strip())

    def list_file_names(self):
        return []

    def get_labelled_blob(self, container_name: str, parent: str, file_name: str, expiry_hours: int = 1)-> LabelledBlob :
        """
        Returns an object with a download url and labels array
        :param container_name: One of the container_names
        :type: str
        :param file_name: Name of the file
        :type: str
        :param parent: Directory in blob storage.
        :type: str
        :param expiry_hours: How long the SAS token will last for
        :type: int
        """
        full_name = join_parent_and_file_name(parent, file_name)
        print(full_name)
        labels_full_name = join_parent_and_file_name_labels(parent, file_name)
        labels_blob = self.blob_service.get_blob_to_text(container_name, labels_full_name)
        labels = labels_blob.content.split('\n')
        sas = self.blob_service.generate_blob_shared_access_signature( 
            container_name, full_name, 
            permission=BlobPermissions.READ,
            expiry=datetime.utcnow() + timedelta(hours=expiry_hours))

        url = self.blob_service.make_blob_url(container_name, full_name, sas_token=sas)
        res = LabelledBlob(url, labels)
        return res

