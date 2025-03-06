# Python image as base
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the FastAPI application
CMD ["python", "-m", "uvicorn", "analyticsAPI:app", "--host", "0.0.0.0", "--port", "8000"]