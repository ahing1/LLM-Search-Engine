# Use Python 3.9+ as the base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy files to container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "backend.api.search_api:app", "--host", "0.0.0.0", "--port", "8000"]
