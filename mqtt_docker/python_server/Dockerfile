FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available
EXPOSE 5000

# Copy all application files
COPY . .

# Set environment variables for Python and Flask
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=app.py
# For better logging in production
ENV FLASK_ENV=production

# Run the application with Python directly instead of Flask CLI
# This gives better control over the application and logging
CMD ["python", "-u", "app.py"]