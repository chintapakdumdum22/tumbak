# Use official Python image as a base
FROM python:3.9-slim

# Set environment variables to avoid issues with input prompts
ENV DEBIAN_FRONTEND=noninteractive

# Create a directory for the app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install necessary system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ffmpeg \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install N_m3u8DL-RE (assuming Linux binary available)
RUN wget https://github.com/nilaoda/N_m3u8DL-RE/releases/download/3.0.0/N_m3u8DL-RE_Linux -O /usr/local/bin/N_m3u8DL-RE \
    && chmod +x /usr/local/bin/N_m3u8DL-RE

# Install Python dependencies from requirements.txt
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Flask
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]
