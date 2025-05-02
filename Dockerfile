# Use Python 3.8 slim image as base
FROM python:3.8-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  gcc \
  python3-dev \
  libpq-dev \
  git \
  && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt requirements-dev.txt ./

# Install dependencies and development tools
RUN pip install --no-cache-dir -r requirements-dev.txt \
  && pip install --no-cache-dir pre-commit

# Copy project files
COPY . .

# Install pre-commit hooks
RUN git init && pre-commit install --install-hooks

# Set up entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["python", "listings/manage.py", "runserver", "0.0.0.0:8000"] 