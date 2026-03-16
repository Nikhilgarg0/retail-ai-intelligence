# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port (adjust if your app uses a different port)
EXPOSE 8501

# Default command to run the dashboard
CMD ["python", "run_dashboard.py"]
