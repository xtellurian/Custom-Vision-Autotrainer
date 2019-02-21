
from autotrainer.custom_vision.custom_vision_client import CustomVisionClient, create_cv_client
from autotrainer.blob.blob_client import BlobClient, create_blob_client_from_connection_string
from autotrainer.blob.models.container import Container
from autotrainer.local.file_loader import list_paths

class Autotrainer:

    custom_vision: CustomVisionClient
    blob: BlobClient
    def __init__(self, cv_key: str, cv_endpoint: str, storage_connection_string:str):
        self.custom_vision = create_cv_client(cv_endpoint, cv_key)
        self.blob = create_blob_client_from_connection_string(storage_connection_string)

    def get_file_paths(self, directory_path: str, ext: str = '')->[str]:
        return list_paths(directory_path, ext)

    def upload_images(self, container: Container, image_paths: [str], labels: [str], parent: str = None):
        for path in image_paths:
            self.blob.add_data_from_path(container.value, path, labels, parent )

    def add_all_images_to_cv(self, container: Container, projectId: str):
        labelled_blobs = self.blob.list_all_labelled_blobs(container.value)
        project = self.custom_vision.training_client.get_project(projectId)
        images = self.custom_vision.create_image_url_list(project, labelled_blobs)
        images = self.custom_vision.balance_images(images)
        self.custom_vision.add_images_to_project(project, images )
        # todo