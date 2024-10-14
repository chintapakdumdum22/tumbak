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
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libaio-dev \
    build-essential \
    ffmpeg \
    aria2 \
    python3-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv /venv

# Set the PATH to the virtual environment
ENV PATH="/venv/bin:$PATH"

# Copy your application code
COPY . /app/
WORKDIR /app/

# Install Python packages
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt

# Command to run your application
CMD ["python", "telegram_bot.py"]
