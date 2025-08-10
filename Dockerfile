# Use Python 3.11 slim as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    nodejs \
    npm \
    ffmpeg \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy package.json and install Node.js dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source code
COPY . .

# Build Tailwind CSS
RUN npm run build:css:once

# Create necessary directories
RUN mkdir -p uploads logs

# Create non-root user
RUN useradd -m -u 1000 metamode && chown -R metamode:metamode /app
USER metamode

# Expose port
EXPOSE 8000

# Copy initialization script
COPY scripts/init_docker.py /app/scripts/

# Start script that initializes DB (if AUTO_INIT_DB=true) and runs the application
CMD ["sh", "-c", "python scripts/init_docker.py && uvicorn src.main:app --host 0.0.0.0 --port 8000"]