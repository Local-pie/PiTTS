FROM python:3.10-slim

WORKDIR /app

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy Frontend code and HTML
COPY main.py .
COPY index.html .

EXPOSE 8000

# 3. Run the API on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
