# Custom-Vision-Autotrainer
An autotraining tool for customvision.ai using Azure Blob Storage and Azure Pipelines

## Features

 * Data Catalogue
 * Train, Test, and Holdout sets
 * CLI, Python and CI/CD friendly
 * Get started quickly with local uploads
 * Store labels with images
 * Select data for training Custom Vision models
 * Train and export your models

### Data Catalogue

Backed by [Azure Storage](https://azure.microsoft.com/en-au/services/storage/), Autotrainer helps you maintain a large collection of labelled images for machine learning.

### Train, Test, and Holdout sets

Machine learning often requires the use of multiple datasets that must remain segregated. Autotrainer provides three containers for image datasets: train, test, and holdout.

 * Train: Used to training the model.
 * Test:  Used to test the model during training, and potentially join the training set.
 * Holdout: Validate your model using this unseen data.

### CLI, Python and CI/CD Friendly

Consume autotrainer via the CLI, in Python code, or run in [Azure Pipelines](https://azure.microsoft.com/en-au/services/devops/pipelines/).

### Get started quickly

Upload a set of images from a directory in a single command.

### Store labels with images

Labels are stored in special *label* files, right next to the image in blob storage.

### Select data for a Custom Vision project

Select images from your training set, and push them to a Custom Vision project.

### Train and export your models

Automate the training and exporting of models.


# Tests

Run tests with

```
nosetests
``` 