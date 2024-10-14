# Use an appropriate base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Clone your GitHub repository
RUN git clone https://github.com/chintapakdumdum22/tumbak .

# Install N_m3u8DL-RE
RUN wget https://github.com/DevLARLEY/N_m3u8DL-RE/releases/download/v0.2.1.2-beta/N_m3u8DL-RE_Beta_linux-x64_20241014.tar.gz && \
    tar -xzvf N_m3u8DL-RE_Beta_build-linux-x64_20241014.tar.gz && \
    chmod +x N_m3u8DL-RE

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 8080

# Run your application
CMD ["python", "telegram_bot.py"]
