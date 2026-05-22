FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --timeout 100 --retries 5

# Copy project files
COPY . .

# Expose application port
EXPOSE 5000

# Start FastAPI app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]