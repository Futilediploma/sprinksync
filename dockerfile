FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc python3-dev libpq-dev netcat-openbsd

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port 8000
EXPOSE 8000

# Run the server
CMD ["sh", "-c", "./wait-for-it.sh db -- python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
