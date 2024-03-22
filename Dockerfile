# Use a specific version of the Python base image
FROM python:3.10-slim as base

# Set the working directory in the container
WORKDIR /app

# Install the project dependencies
FROM base as build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Final stage
FROM base
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .

# Add labels for metadata
# LABEL maintainer="Your Name <your@email.com>"
# LABEL description="FastAPI application"

# Expose the port that the FastAPI server will run on
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]