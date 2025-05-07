# Use an official Python image
FROM python:3.11-slim

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files to container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Start app
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
