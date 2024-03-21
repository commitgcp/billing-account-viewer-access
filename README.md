# Sales Billing Account Access App


Overview

The Billing Account Viewer Permissions App is a Streamlit-based web application designed to streamline the process of granting billing account viewer permissions to specified email addresses within the Google Cloud Platform (GCP). This app automates the selection of billing accounts and the assignment of viewer permissions, minimizing manual effort and potential for error.


Features

    Email Validation: Users can enter an email address, which the app validates in real-time to ensure it conforms to standard email formatting.
    Billing Account Selection: Once an email is confirmed, users can select one or more billing accounts from a dynamically populated list to which the viewer permissions will be granted.
    Terraform Integration: The app utilizes Terraform (pretf) to generate and apply infrastructure as code, ensuring permissions are set consistently and auditably across selected billing accounts.
    Real-Time Feedback: Users receive immediate feedback during each step of the process, including the execution of Terraform plans and the application of permissions.


Prerequisites

To use and manage the Billing Account Viewer Permissions App effectively, you should have:

    Basic understanding of GCP billing accounts and IAM permissions.
    Familiarity with Terraform for infrastructure management.
    Access to a the a GCP project with permissions to create and manage Cloud Build and Cloud Run services, and to assign IAM roles to billing accounts. This project uses the "commit-automation" GCP project - if you want to run it as-is, you must request project permissions from the Commit GCP team.

Usage

Starting the App

    Access the web application through the provided URL: https://34.117.63.81.sslip.io/
    Enter a valid email address for the user who will receive billing viewer permissions.
    Confirm the email address, and select the billing accounts from the presented list.
    Review the Terraform plan detailing the permissions to be applied.
    Confirm to apply the changes. Terraform will execute the plan, granting the specified permissions.


Managing Permissions

The app provides an interface to select billing accounts and assign viewer permissions to a specified email. These permissions can be managed through the GCP console if adjustments are needed after initial setup.


Deployment

The app is containerized using Docker, allowing for deployment in various environments, including GCP's Cloud Run service. The provided Dockerfile and cloudbuild.yaml facilitate the building and deployment process.
Building the Container

To build the Docker container image, use the following command from the root project directory:

gcloud builds submit --region=me-west1 --config cloudbuild.yaml


Deploying to Cloud Run

After the container image is built, deploy it to Cloud Run manually through the GCP console or using the gcloud CLI, ensuring the service is accessible.


For issues not covered in this documentation, please refer to the following resources:

    Streamlit Documentation
    Terraform Documentation
    Google Cloud IAM Documentation