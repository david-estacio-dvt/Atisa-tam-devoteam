FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . .

# Environment variables (Defaults, can be overridden by Cloud Run)
ENV PORT=8080

# Run Streamlit on port 8080
CMD streamlit run ui/app.py --server.port 8080 --server.address 0.0.0.0
