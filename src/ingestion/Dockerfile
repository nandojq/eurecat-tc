# Use Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /ingestion

# Copy the current directory contents into the container 
COPY . /ingestion

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["python", "ingestion.py"]
