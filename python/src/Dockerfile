# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Install required packages for Selenium and Chrome
RUN apt-get update && apt-get install -y \
    wget \
	curl \
    unzip \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium


# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Command to run the scraper
CMD ["python", "autorundaemon.py"]
