FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    nginx \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Copy nginx configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Download Cloud SQL Proxy (for GCP deployment)
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O /app/cloud_sql_proxy && \
    chmod +x /app/cloud_sql_proxy || echo "Cloud SQL Proxy download failed, will use direct connection"

# Copy startup script
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expose port
EXPOSE 80

CMD ["/app/start.sh"]
