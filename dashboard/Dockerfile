FROM python:3.11-slim

WORKDIR /dashboard

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy dashboard files
COPY dashboard/ .

# Expose the port the app will run on
EXPOSE 5001

# Command to run the application
CMD ["python", "app.py"]
