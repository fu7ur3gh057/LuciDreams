# Use the official Python image as the base image
FROM python:3.10.9-bullseye

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app/backend

# Copy the requirements file to the working directory
COPY ./requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Make the entrypoint script executable
RUN chmod +x ./deploy/entrypoint.sh

# Expose the port that the application will use
EXPOSE 8500

# Set the entrypoint to execute the server-entrypoint.sh script
ENTRYPOINT ["./deploy/entrypoint.sh"]