FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything including the artifacts folder
COPY . .

# Verify model file exists (this will fail the build if it doesn't)
RUN test -f artifacts/model/lgbm_model.pkl || echo "WARNING: Model file not found!"

RUN if [ -f setup.py ] || [ -f pyproject.toml ]; then \
      pip install --no-cache-dir -e .; \
    fi

EXPOSE 8080

CMD ["python3", "app.py"]