import os
import unittest

from autotrainer.blob.models.container import Container
from autotrainer.autotrainer import Autotrainer
from autotrainer.custom_vision.domain import Domain
from autotrainer.custom_vision.classification_type import ClassificationType

# conn_string='DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;'
conn_string=os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']
cv_endpoint="https://australiaeast.api.cognitive.microsoft.com"
CVTK=os.environ['CUSTOMVISIONTRAININGKEY']
rians_dir = "C:/data/scotts-data/Capture3/banana_organic"

class AutotrainerTests(unittest.TestCase):
    autotrainer: Autotrainer
    def setUp(self):
        self.autotrainer = Autotrainer(CVTK,cv_endpoint,conn_string)
        self.autotrainer.blob.initialise_containers()

    # def tearDown(self):
    #     containers = self.autotrainer.blob.blob_service.list_containers()
    #     for c in containers:
    #         self.autotrainer.blob.blob_service.delete_container(c.name)

    def test_upload_files(self):
        image_paths = self.autotrainer.get_file_paths(rians_dir, 'png')
        for path in image_paths:
            self.autotrainer.blob.add_data_from_path(Container.test.name, path )

    def test_add_images_to_project(self):
        project = self.autotrainer.custom_vision.create_project(
            'test_add_images',
            'created by unit test', 
            Domain.GENERAL_CLASSIFICATION, 
            ClassificationType.MULTICLASS )
        image_paths = self.autotrainer.get_file_paths(rians_dir, 'png')
        for path in image_paths:
            self.autotrainer.blob.add_data_from_path(Container.test.name, path, ['banana'])
        
        self.autotrainer.add_all_images_to_cv(Container.test, project.id)