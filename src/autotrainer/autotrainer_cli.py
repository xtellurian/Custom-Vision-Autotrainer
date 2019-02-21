import os
import argparse
import sys
import time

from autotrainer.autotrainer import Autotrainer
from autotrainer.custom_vision.domain import Domain
from autotrainer.custom_vision.classification_type import ClassificationType

class AutotrainerCli:
    cv_key: str
    cv_endpoint: str
    storage_connection_string: str
    autotrainer: Autotrainer
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Pretends to be git',
            usage='something')

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
        else:
            print('Incorrect syntax')

    def blob(self):
        # define the CLI args
        parser = argparse.ArgumentParser(description='Train a custom vison model')
        parser.add_argument('cv_projectId', help='Custom Vision project id')

        # parser.add_argument('--tagStrategy', help='How to tag, eg: article, segment, or segment/article')
        # parser.add_argument('--segmentId', nargs='?', help='Only get images from this segment') # optional

        args = parser.parse_args()

        autotrainer = Autotrainer(args.cv_key, args.cv_endpoint, args.connection_string )

        storage_info = autotrainer.blob.blob_service.get_blob_account_information()
        print(storage_info)
        cv_projects=autotrainer.custom_vision.training_client.get_projects()
        print(cv_projects)



if __name__ == '__main__':
    AutotrainerCli()