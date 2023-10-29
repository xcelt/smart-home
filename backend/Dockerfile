# Set base image (host OS)
FROM python:3.10.13-bookworm

# Set environment variable to show python output in terminal instead of buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /backend

# Copy the dependencies file to the working directory
COPY ../requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy from current directory of Dockerfile to /backend in the image
COPY . .

EXPOSE 8000