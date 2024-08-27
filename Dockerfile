FROM python:bullseye

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libmariadb-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /know

# Copy the current directory contents into the container at /know
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8005 available to the world outside this container
EXPOSE 8005

# Define environment variable
ENV NAME=knowemployee

# Run app.py when the container launches
#CMD ["uvicorn", "knowemployee:app", "--host", "0.0.0.0", "--port", "8005", "--log-level", "debug"]
CMD ["gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8005", "wsgi:app", "-c", "gunicorn.conf.py"]