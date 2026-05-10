FROM python:3.10-slim

# 1. Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy the pre-downloaded models and piper binary
COPY download_assets.py .
RUN python download_assets.py
RUN ls -la

# Add the extracted Piper binary to the system PATH
# Note: The tar extraction creates a subfolder called "piper"
ENV PATH="/models/piper:${PATH}"

# Ensure piper is executable
RUN chmod +x /models/piper/piper

# 3. Copy our application code
COPY main.py .

# 4. Run the API on port 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
