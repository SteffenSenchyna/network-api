# First stage: Build stage
FROM python:3.9.2-alpine3.13 as builder

# Upgrade pip and install build dependencies
RUN pip install --upgrade pip && \
    pip install --upgrade wheel setuptools && \
    apk upgrade && \
    apk add --update gcc musl-dev libffi-dev libressl-dev

# Copy requirements and install dependencies
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy the rest of the application
COPY . /app

# Run unit tests
RUN python -m unittest discover -s tests -p "*_test.py"


# Second stage: Runtime stage
FROM python:3.9.2-alpine3.13

# Copy the built dependencies from the first stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the application
COPY . /app
WORKDIR /app

# Expose port and run the application
EXPOSE 8081/TCP
CMD [ "python", "-u", "api.py" ]
