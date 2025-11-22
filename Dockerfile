FROM python:slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# OS deps
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# (A) If you have requirements.txt, prefer this:
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# (B) If you truly need editable install (pyproject/setup.py present), keep -e .
COPY . .
RUN pip install --no-cache-dir -e .

# ❌ Don't train at build time
# RUN python3 pipeline/training_pipeline.py

EXPOSE 8080
CMD ["python3", "app.py"]
