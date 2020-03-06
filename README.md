# Sprinter
A package to distribute python processing on Google Cloud Run

I needed a way to distribute and execute in parallel a large number of small tasks. This tool uses Google cloud functions to achieve this.

## Setup 
Setup the project and region you will be using in your gcloud console
```
gcloud init
```

Initialize your GCP project
```
make init_project
```
This should set everything up for you: credentials, env file, the necessary infrastructure on your project, etc 

## Run
Execute a dummy job
```
make run
```