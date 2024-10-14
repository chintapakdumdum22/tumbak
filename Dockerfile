FROM ubuntu:22.04

# Install required system packages
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    python3-pip \
    python3-dev \
    libffi-dev \
    libssl-dev \
    ffmpeg \
    aria2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code
COPY . /app/
WORKDIR /app/

# Install Python packages
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

# Command to run your application
CMD ["python3", "telegram_bot.py"]
