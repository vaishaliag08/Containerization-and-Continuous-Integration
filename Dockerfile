# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory /app in the container
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed dependencies specified in the file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to run the flask app
EXPOSE 5000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Run app.py when the container launches
CMD ["python", "app.py"]