#!/bin/bash

GCP_PROJECT_NAME="your-project-name"
gcloud config set project $GCP_PROJECT_NAME

DOCKER_IMG="gcr.io/$GCP_PROJECT_NAME/tone"
echo $DOCKER_IMG
gcloud builds submit --tag $DOCKER_IMG
