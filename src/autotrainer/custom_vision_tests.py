
import os
import unittest
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import Project, ImageUrlCreateEntry

from autotrainer.blob.blob_client import LabelledBlob

from autotrainer.custom_vision.custom_vision_client import CustomVisionClient
from autotrainer.custom_vision.domain import Domain
from autotrainer.custom_vision.classification_type import ClassificationType

CVTK=os.environ['CUSTOMVISIONTRAININGKEY']
training_client = CustomVisionTrainingClient(CVTK, 'https://australiaeast.api.cognitive.microsoft.com')

class CustomVisionTests(unittest.TestCase):
    project: Project
    def setUp(self):
        self.project = training_client.create_project('unit-tests')
    
    def tearDown(self):
        training_client.delete_project(self.project.id)

    def test_create_project(self):
        client = CustomVisionClient(training_client)
        project = client.create_project('test', 'test', Domain.GENERAL_CLASSIFICATION, ClassificationType.MULTICLASS)
        self.assertIsNotNone(project)
        self.assertIsInstance(project, Project)
        self.assertEqual(project.name, 'test')
        projects = training_client.get_projects()
        self.assertIn(project, projects)
        training_client.delete_project(project.id)

    def test_create_image_url_list(self):
        client = CustomVisionClient(training_client)
        labelled_blobs = [LabelledBlob('url1', ['tomato','potato']), LabelledBlob('url2', ['banana','fig'])]
        image_urls = client.create_image_url_list(self.project, labelled_blobs )
        for labelled_blob in labelled_blobs:
            self.assertIn(labelled_blob.download_url, [i.url for i in image_urls])
        for image in image_urls:
            self.assertIsInstance(image, ImageUrlCreateEntry)