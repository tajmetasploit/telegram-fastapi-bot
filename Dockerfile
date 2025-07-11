# Use official Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Run uvicorn server by default (can be overridden)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", 8000]
