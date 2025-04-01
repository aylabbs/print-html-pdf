# Dockerfile

FROM python:3.10-slim

# Install system packages needed by WeasyPrint (fonts, cairo, pango, etc.)
RUN apt-get update && apt-get install -y \
    libffi-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libjpeg62-turbo-dev \
    libpng16-16 \
    pango1.0-tools \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Create and use a dedicated directory
WORKDIR /app

# Copy in requirements first (for Docker layer caching)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the FastAPI app
COPY app.py /app/

# Expose the port inside the container
EXPOSE 8000

# Run the FastAPI app with Uvicorn on port 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
