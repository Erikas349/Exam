# === Builder stage ===
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install to local user path
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Make sure everything is readable and executable
RUN chmod -R 755 /app

# === Final stage ===
FROM python:3.12-slim

# Add non-root user
RUN adduser --disabled-password --gecos "" appuser

# Create working directory with proper permissions
WORKDIR /home/appuser/app
RUN mkdir -p /home/appuser/app && chown -R appuser:appuser /home/appuser

# Copy installed dependencies from builder
COPY --from=builder /root/.local /home/appuser/.local

# Copy the application code
COPY --from=builder /app /home/appuser/app

# Set environment variables for PATH and PYTHONPATH
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONPATH=/home/appuser/.local/lib/python3.12/site-packages

# Set non-root user
USER appuser

# Expose Flask port
EXPOSE 5000

# Start the application
CMD ["python", "app.py"]