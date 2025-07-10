# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Make sure start.sh is executable
RUN chmod +x ./start.sh

# Expose FastAPI default port
EXPOSE 8000

# Run the start.sh script to launch FastAPI and the bot
CMD ["./start.sh"]
