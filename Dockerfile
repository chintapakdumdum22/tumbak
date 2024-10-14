FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install dependencies including git and make
RUN apt-get update && apt-get install -y git make && \
    # Clone the N_m3u8DL-RE repository
    git clone https://github.com/n_m3u8DL-RE/n_m3u8DL-RE.git && \
    # Change into the cloned directory and install it
    cd n_m3u8DL-RE && \
    make install && \
    # Clean up the installation files
    rm -rf n_m3u8DL-RE

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code
COPY . .

# Run the bot
CMD ["python", "telegram_bot.py"]
