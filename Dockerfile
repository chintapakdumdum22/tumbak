FROM ubuntu:22.04

# Install required system packages
RUN apt-get update -y && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends gcc libffi-dev musl-dev ffmpeg aria2 python3-pip python3-dev \
    && apt-get install -y python3-aiohttp \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

# Install Python packages
RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt

CMD ["python3", "telegram_bot.py"]
