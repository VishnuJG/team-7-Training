FROM python:3.7
# Run commands from /app directory inside container
WORKDIR /app
# Copy requirements from local to docker image
COPY requirements.txt /app
# Install the dependencies in the docker image
RUN pip3 install -r requirements.txt --no-cache-dir
# Copy everything from the current dir to the image
COPY . .
# Run the gunicorn server on top of the flask app
RUN CMD["gunicorn", "--workers", "9", "--bind", "0.0.0.0:5002", "wsgi:app"]