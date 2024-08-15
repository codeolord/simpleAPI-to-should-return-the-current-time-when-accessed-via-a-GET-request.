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