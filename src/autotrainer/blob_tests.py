import os
import uuid
import unittest
from azure.storage.blob import BlockBlobService
from autotrainer.blob.blob_client import BlobClient

conn_string='DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://localhost:10000/devstoreaccount1;'
block_blob_service = BlockBlobService(connection_string=conn_string)
test_file_name = 'sample.jpg'
test_file = os.path.join( os.path.dirname(os.path.abspath(__file__)), test_file_name)


class InitBlobTests(unittest.TestCase):

    def tearDown(self):
        containers = block_blob_service.list_containers()
        for c in containers.items:
            block_blob_service.delete_container(c.name)

    def test_initialise_containers(self):
        blob_client=BlobClient(block_blob_service)
        blob_client.initialise_containers()

        containers = block_blob_service.list_containers()
        for n in blob_client.container_names:
            self.assertIn(n, [ c.name for c in containers.items])

class BlobTests(unittest.TestCase):

    parent_prefix= str(uuid.uuid4())
    test_container=str(uuid.uuid4()) + '-test'

    def setUp(self):
        block_blob_service.create_container(self.test_container)
    
    def tearDown(self):
        block_blob_service.delete_container(self.test_container)
    
    def test_add_training_from_path(self):
        blob_client=BlobClient(block_blob_service)
        parent =  self.parent_prefix + '1'
        blob_client.add_data_from_path(self.test_container, test_file, parent, ['dog'])

        blobs = block_blob_service.list_blobs(self.test_container)
        print([c.name for c in blobs.items])
        self.assertIn(parent + '/sample.jpg', [c.name for c in blobs.items])
        self.assertIn(parent + '/sample.jpg.labels', [c.name for c in blobs.items])

    def test_get_labelled_blob(self):
        blob_client=BlobClient(block_blob_service)
        parent = self.parent_prefix + '2' 
        labels = ['dog', 'cat']
        blob_client.add_data_from_path(self.test_container, test_file, parent , labels)
        labelled_blob = blob_client.get_labelled_blob(self.test_container, parent, test_file_name)
        self.assertEqual(labelled_blob.labels, labels)

    if __name__ == '__main__':
        unittest.main()