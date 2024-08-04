# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get install -y python3-dev \
    && apt-get install -y libpq-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files to the docker environment
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000

# Run the command to start the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]