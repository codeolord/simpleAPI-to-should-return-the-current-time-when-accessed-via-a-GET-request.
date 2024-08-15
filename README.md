# Simple Time API

## Overview
This project is a simple API that returns the current time in UTC when accessed via a GET request. The API is containerized using Docker and deployed to Google Cloud Platform (GCP) using Kubernetes (GKE) and Terraform. A CI/CD pipeline is implemented with GitHub Actions to automate the deployment process.

## Project Structure

```plaintext
├── app.py              # The API source code
├── Dockerfile          # Dockerfile to containerize the API
├── requirements.txt    # Python dependencies
├── terraform/          # Terraform code for infrastructure setup
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
├── .github/workflows/  # GitHub Actions workflow for CI/CD
│   └── deploy.yml
└── README.md           # Project documentation

steps of the project, from setting up your development environment to deploying the API on GCP using Kubernetes, Terraform, and GitHub Actions.

Setting up the Local Development Environment
Install Prerequisites:

Docker: Install Docker
Google Cloud SDK: Install Google Cloud SDK
Terraform: Install Terraform
Python 3.9+: Install Python
Set Up Google Cloud:

Created a new GCP project.
Enable billing for the project.
Enable the Google Kubernetes Engine API.

Develop the Simple Time API
Create the Project Directory:

bash
Copy code
mkdir simple-time-api
cd simple-time-api
Create the API:

Create a file named app.py with the following content:
python
Copy code
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/time', methods=['GET'])
def get_time():
    current_time = datetime.utcnow().isoformat() + "Z"
    return jsonify({"current_time": current_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
Create the requirements.txt File:

Add the following content:
txt
Copy code
Flask==2.0.1
Step 3: Containerize the API using Docker
Create the Dockerfile:

Create a file named Dockerfile in the project root:
Dockerfile
Copy code
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "app.py"]
Build and Test the Docker Image Locally:

Ran the following commands:
bash
Copy code
docker build -t simple-api .
docker run -p 8080:8080 simple-api
Visit http://localhost:8080/time to see the JSON response.
Step 4: Set Up Google Container Registry (GCR)
Authenticate Docker to GCR:

Run:
bash
Copy code
gcloud auth configure-docker
Tag and Push the Docker Image to GCR:

Replace your-gcp-project-id with your actual project ID:
bash
Copy code
docker tag simple-api gcr.io/your-gcp-project-id/simple-api
docker push gcr.io/your-gcp-project-id/simple-api
Step 5: Write Terraform Configuration for GCP Infrastructure
Create a Terraform Directory:

bash
Copy code
mkdir terraform
cd terraform
Create Terraform Files:

main.tf: Define the GKE cluster and related resources.
hcl
Copy code
provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_container_cluster" "primary" {
  name     = "gke-cluster"
  location = var.region

  node_config {
    machine_type = "e2-medium"
  }

  initial_node_count = 3
}
variables.tf: Define variables for the project.
hcl
Copy code
variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}
outputs.tf: Outputs for your resources.
hcl
Copy code
output "kubernetes_cluster_name" {
  value = google_container_cluster.primary.name
}
Step 6: Set Up Kubernetes Resources in Terraform
Add Kubernetes Resources in main.tf:

hcl
Copy code
resource "kubernetes_namespace" "example" {
  metadata {
    name = "example-namespace"
  }
}

resource "kubernetes_deployment" "api_deployment" {
  metadata {
    name      = "api-deployment"
    namespace = kubernetes_namespace.example.metadata[0].name
  }

  spec {
    replicas = 3

    selector {
      match_labels = {
        app = "simple-api"
      }
    }

    template {
      metadata {
        labels = {
          app = "simple-api"
        }
      }

      spec {
        container {
          name  = "simple-api"
          image = "gcr.io/${var.project_id}/simple-api"
          ports {
            container_port = 8080
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "api_service" {
  metadata {
    name      = "api-service"
    namespace = kubernetes_namespace.example.metadata[0].name
  }

  spec {
    selector = {
      app = kubernetes_deployment.api_deployment.spec[0].template[0].metadata[0].labels.app
    }
    type = "LoadBalancer"
    port {
      port = 80
      target_port = 8080
    }
  }
}
Step 7: Implement GitHub Actions for CI/CD
Create GitHub Actions Workflow:

Inside your repository, create .github/workflows/deploy.yml.
yaml
Copy code
name: GKE Deploy

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Google Cloud SDK
      uses: google-github-actions/setup-gcloud@v0.2.0
      with:
        service_account_key: ${{ secrets.GCP_CREDENTIALS }}
        project_id: ${{ secrets.GCP_PROJECT_ID }}

    - name: Authenticate Docker to Google Container Registry
      run: gcloud auth configure-docker

    - name: Build Docker image
      run: docker build -t gcr.io/${{ secrets.GCP_PROJECT_ID }}/simple-api .

    - name: Push Docker image to GCR
      run: docker push gcr.io/${{ secrets.GCP_PROJECT_ID }}/simple-api

    - name: Run Terraform
      run: terraform init && terraform apply -auto-approve
Step 8: Push Code to GitHub and Deploy
Initialize Git and Add Files:

bash
Copy code
git init
git add .
git commit -m "Initial commit with API, Docker, and Terraform setup"
Push to GitHub:

bash
Copy code
git remote add origin https://github.com/azurefarmer/your-repo-name.git
git branch -M main
git push -u origin main
Check GitHub Actions:

