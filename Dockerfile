# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose ports
EXPOSE 8000 8501

# Create entrypoint script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting Mitra AI Recommendation Assistant..."\n\
python main.py &\n\
streamlit run app.py --server.port=8501 --server.address=0.0.0.0' > /app/start.sh

RUN chmod +x /app/start.sh

# Set environment variables
ENV FASTAPI_HOST=0.0.0.0
ENV FASTAPI_PORT=8000

# Run the application
CMD ["/app/start.sh"]
