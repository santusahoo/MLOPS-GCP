FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

# Install OS dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install the package if needed
RUN if [ -f setup.py ] || [ -f pyproject.toml ]; then \
      pip install --no-cache-dir -e .; \
    fi

EXPOSE 8080

# Use gunicorn for production (already in your requirements from mlflow)
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app