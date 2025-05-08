# Use slim base image
FROM python:3.10-slim

# ✅ Install required system libs for OpenCV + Ultralytics
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set app working directory
WORKDIR /app

# Copy your project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 8000

# Start using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
