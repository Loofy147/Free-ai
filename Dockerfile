# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the dependency files to the working directory
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy the rest of the application's code to the working directory
COPY . .

# Set the command to run when the container starts
CMD ["python", "main.py"]
