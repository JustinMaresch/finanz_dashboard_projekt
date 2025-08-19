FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/
COPY app/templates/ app/templates/
COPY app/static/ app/static/


RUN mkdir -p /app/logs

EXPOSE 5000

CMD ["python", "app/app.py"]
