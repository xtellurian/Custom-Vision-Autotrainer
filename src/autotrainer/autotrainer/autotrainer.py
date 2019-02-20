
from autotrainer.custom_vision.custom_vision_client import CustomVisionClient, create_cv_client
from autotrainer.blob.blob_client import BlobClient, create_blob_client_from_connection_string
from autotrainer.blob.models.container import Container
from autotrainer.local.file_loader import list_paths

class Autotrainer:

    custom_vision: CustomVisionClient
    blob: BlobClient
    def __init__(self, cv_key: str, cv_endpoint: str, storage_connection_string:str):
        self.custom_vision = create_cv_client(cv_key, cv_endpoint)
        self.blob = create_blob_client_from_connection_string(storage_connection_string)

    def get_file_paths(self, container: Container, directory_path: str, ext: str)->[str]:
        return list_paths(directory_path, ext)

    def add_all_images_to_cv(self, container: Container):
        labelled_blobs = self.blob.list_all_labelled_blobs(container.name)
        # todo