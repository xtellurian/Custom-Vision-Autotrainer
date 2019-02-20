import unittest

from autotrainer.blob.models.container import Container
from autotrainer.autotrainer import Autotrainer

conn_string='DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;'

rians_dir = "C:/data/scotts-data/Capture3/banana_organic"
class AutotrainerTests(unittest.TestCase):
    autotrainer: Autotrainer
    def setUp(self):
        self.autotrainer = Autotrainer('','',conn_string)
        self.autotrainer.blob.initialise_containers()

    def test_upload_files(self):
        
        image_paths = self.autotrainer.get_file_paths(Container.test, rians_dir, 'png')
        for path in image_paths:
            self.autotrainer.blob.add_data_from_path(Container.test.name, path )
