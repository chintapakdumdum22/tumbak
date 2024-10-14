FROM python:3.10  # Use a specific version of Python

# Install required system packages
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libaio-dev \
    build-essential \
    ffmpeg \
    aria2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app/

# Copy your application code
COPY . .

# Install Python packages
RUN pip install --no-cache-dir --upgrade --requirement requirements.txt

# Command to run your application
CMD ["python", "telegram_bot.py"]
