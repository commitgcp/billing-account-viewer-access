FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for Terraform and other utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        unzip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set Terraform version and download location
ENV TERRAFORM_VERSION=1.7.4

# Download, unzip, and move the Terraform binary to a location within the system's PATH
RUN wget https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && unzip terraform_${TERRAFORM_VERSION}_linux_amd64.zip \
    && mv terraform /usr/local/bin/ \
    && rm terraform_${TERRAFORM_VERSION}_linux_amd64.zip

# Copy the requirements.txt file to the working directory
COPY ./requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the working directory
COPY . .

# Expose the port on which the app will run
EXPOSE 8501

# Start the app
CMD ["python3", "-m", "streamlit", "run", "app.py"]