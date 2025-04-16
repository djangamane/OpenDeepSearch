FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy the OpenDeepSearch code
COPY . .

# Install the package in development mode
RUN pip install -e .

# Expose the API port
EXPOSE 8000

# Command to run the API
CMD ["python", "opendeepsearch_api.py"] 