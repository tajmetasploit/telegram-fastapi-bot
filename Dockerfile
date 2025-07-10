# Use official Python runtime as base image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Run FastAPI directly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

worker: python app/bot.py

