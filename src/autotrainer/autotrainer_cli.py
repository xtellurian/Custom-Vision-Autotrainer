import os
import argparse
import sys
import time

from autotrainer.autotrainer import Autotrainer
from autotrainer.custom_vision.domain import Domain
from autotrainer.custom_vision.classification_type import ClassificationType
from autotrainer.custom_vision.platform import Platform, Flavour
from autotrainer.blob.models.container import Container

class AutotrainerCli:
    cv_key: str
    cv_endpoint: str
    storage_connection_string: str
    autotrainer: Autotrainer
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Autotrainer tools',
            usage='autotrainer [cv, upload] <options>')

        parser.add_argument('command', help='Subcommand to run')
        # parse_args defaults to [1:] for args, but you need to
        # exclude the rest of the args too, or validation will fail
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        
        # setup the keys from environment variables
        self.cv_key = os.environ['CV_TRAINING_KEY']
        self.cv_endpoint=os.environ['CV_ENDPOINT']
        self.storage_connection_string=os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']
        self.autotrainer = Autotrainer(self.cv_key, self.cv_endpoint, self.storage_connection_string)
        
        getattr(self, args.command)() # call the method on this obj

    def cv(self):
        
        parser = argparse.ArgumentParser(
            description='Custom Vision tools')
        # prefixing the argument with -- means it's optional
        parser.add_argument('--newproject', help='Name of the new project. Returns project id')
        parser.add_argument('--domain', type=Domain, choices=list(Domain), default=Domain.GENERAL_CLASSIFICATION)
        parser.add_argument('--type', type=ClassificationType, choices=list(ClassificationType), default=ClassificationType.MULTICLASS)
        parser.add_argument('--project', help='Id of the custom vision project')
        parser.add_argument('--train', help='Train a project. Returns iteration id', action='store_true')
        parser.add_argument('--export', help='Export a project', action='store_true')
        parser.add_argument('--iteration', help='(optional) iteration to store')
        parser.add_argument('--platform', help='Platform to export to', type=Platform, choices=list(Platform), default=Platform.DOCKER)
        parser.add_argument('--flavour', help='Platform dependent Flavour', type=Flavour, choices=list(Flavour), default=Flavour.Linux)
        args = parser.parse_args(sys.argv[2:])
        if(args.newproject):
            print('Creating new project: ' + args.newproject)
            project = self.autotrainer.custom_vision.create_project(args.newproject, 'Created by autotrainer CLI', args.domain, args.type )
            print(project.id)
        elif args.train:
            project = self.autotrainer.custom_vision.training_client.get_project(args.project)
            print('Training project: {}'.format(project.name))
            iteration = self.autotrainer.custom_vision.train_project_and_wait(project)
            print(iteration.id)
        elif args.export:
            project = self.autotrainer.custom_vision.training_client.get_project(args.project)
            if(args.iteration):
                iteration = self.autotrainer.custom_vision.training_client.get_iteration(project.id, args.iteration)
            else:
                iteration = self.autotrainer.custom_vision.training_client.get_iterations(project.id)[0]
            if not iteration.exportable:
                print('Iteration is not exportable')
                exit(1)
            export = self.autotrainer.custom_vision.export_project(args.platform, args.flavour, project, iteration)
            print(export.download_uri)
        else:
            print('Incorrect syntax')

    def upload(self):
        # define the CLI args
        parser = argparse.ArgumentParser(description='Data tools')
        parser.add_argument('-d', '--directory', required=True, help='The local directory containing the images')
        parser.add_argument('-c','--container', type=Container, choices=list(Container), default=Container.train, required=True)
        parser.add_argument('-l', '--labels', action='append', help='Label for the image', required=True)
        parser.add_argument('--extension', help='Filter on file extension', default='')
        parser.add_argument('--parent', help='Parent directory in Blob Storage', default=None)
        # parser.add_argument('--tagStrategy', help='How to tag, eg: article, segment, or segment/article')
        # parser.add_argument('--segmentId', nargs='?', help='Only get images from this segment') # optional

        args = parser.parse_args(sys.argv[2:])
        image_paths = self.autotrainer.get_file_paths(args.directory, args.extension)
        labelled_blobs = self.autotrainer.upload_images(args.container, image_paths, args.labels, args.parent )
        print('Created {} labelled blobs'.format(len(labelled_blobs)))



if __name__ == '__main__':
    AutotrainerCli()