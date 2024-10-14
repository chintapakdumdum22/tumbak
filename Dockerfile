# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Install N_m3u8DL-RE
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://github.com/DevLARLEY/N_m3u8DL-RE/releases/download/v0.2.1.2-beta/N_m3u8DL-RE_Beta_linux-x64_20241014.tar.gz && \
    tar -xzf N_m3u8DL-RE_Beta_linux-x64_20241014.tar.gz && \
    mv N_m3u8DL-RE /usr/local/bin/ && \
    chmod +x /usr/local/bin/N_m3u8DL-RE && \
    rm N_m3u8DL-RE_Beta_linux-x64_20241014.tar.gz

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application
CMD ["python", "telegram_bot.py"]
