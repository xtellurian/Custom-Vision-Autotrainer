
import os
import unittest
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import Project

from autotrainer.custom_vision.custom_vision_client import CustomVisionClient
from autotrainer.custom_vision.domains import Domain
from autotrainer.custom_vision.classification_type import ClassificationType

CVTK=os.environ['CUSTOMVISIONTRAININGKEY']
training_client = CustomVisionTrainingClient(CVTK, 'https://australiaeast.api.cognitive.microsoft.com')

class CustomVisionTests(unittest.TestCase):
    
    # def setUp(self):

    def test_create_project(self):
        client = CustomVisionClient(training_client)
        project = client.create_project('test', 'test', Domain.GENERAL_CLASSIFICATION, ClassificationType.MULTICLASS)
        self.assertIsNotNone(project)
        self.assertIsInstance(project, Project)
        self.assertEqual(project.name, 'test')
        projects = training_client.get_projects()
        self.assertIn(project, projects)
        training_client.delete_project(project.id)