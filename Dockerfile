# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

# Environment settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose the port Django will run on
EXPOSE 8000

# Run the Django development server using your custom manage.py
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

