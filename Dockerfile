# Use a slim Python image for efficiency
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 7860

# Set the working directory
WORKDIR /app

# Install system dependencies (needed for OpenCV, Pillow, and PostgreSQL)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Create a directory for static files and media
RUN mkdir -p /app/staticfiles /app/media

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose the port Hugging Face uses
EXPOSE 7860

# Start the application using Gunicorn
# Hugging Face Spaces require the app to bind to 0.0.0.0:7860
CMD ["gunicorn", "crop_project.wsgi:application", "--bind", "0.0.0.0:7860", "--timeout", "120"]
