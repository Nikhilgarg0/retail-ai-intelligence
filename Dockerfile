# Use official Python image

# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy only requirements first
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only source code and main files
COPY src/ ./src/
COPY run_dashboard.py ./
COPY config/ ./config/

# Expose port (adjust if your app uses a different port)
EXPOSE 8501

# Default command to run the dashboard
CMD ["python", "run_dashboard.py"]
