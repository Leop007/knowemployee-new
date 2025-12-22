FROM python:3.10-alpine

# Install necessary dependencies
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     pkg-config \
#     default-libmysqlclient-dev \
#     libmariadb-dev \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

RUN apk add --no-cache \
    build-base \
    pkgconf \
    mariadb-dev \
    python3-dev 
    
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
CMD ["gunicorn", "wsgi:app", "-c", "gunicorn.conf.py"]