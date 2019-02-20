
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import Project, ImageUrlCreateEntry, Tag

from autotrainer.custom_vision.domains import Domain
from autotrainer.custom_vision.classification_type import ClassificationType
from autotrainer.custom_vision.labeller import Labeller

from autotrainer.blob.blob_client import LabelledBlob

class CustomVisionClient:
    training_client: CustomVisionTrainingClient

    def __init__(self, training_client: CustomVisionTrainingClient):
        self.training_client = training_client

    def create_project(self, name: str, desc: str, domain: Domain, classification_type: ClassificationType)-> Project :
        project = self.training_client.create_project(
            name, 
            description=desc, 
            domain_id=domain.to_id(),
            classification_type=classification_type.to_id())
        return project

    def create_image_url_list(self, project: Project, labelled_blobs: [LabelledBlob])-> [ImageUrlCreateEntry]:
        labeller = Labeller()
        image_url_create_list = []
        for labelled_blob in labelled_blobs:
            tag_ids = []
            for label in labelled_blob.labels:
                tag_ids.append(labeller.add_label_if_not_exists(self.training_client, project, label).id)
            image_url_create_list.append( ImageUrlCreateEntry(url=labelled_blob.download_url, tag_ids=tag_ids ))
        return image_url_create_list

