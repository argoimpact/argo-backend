# Use a specific version of the Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

# Expose the port that the FastAPI server will run on
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
