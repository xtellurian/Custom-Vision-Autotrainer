
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import Project

from autotrainer.custom_vision.domains import Domain
from autotrainer.custom_vision.classification_type import ClassificationType

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