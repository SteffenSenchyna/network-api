# Stage 1: build environment
FROM python:3.9.2-alpine3.13 as builder

# Upgrade pip and install build dependencies
RUN pip install --upgrade pip && \
    pip install --upgrade wheel setuptools && \
    apk upgrade && \
    apk add --update gcc musl-dev libffi-dev libressl-dev

WORKDIR /app
COPY . /app
RUN pip wheel --wheel-dir=/wheels -r requirements.txt
RUN python -m unittest discover -s . -p "*_test.py"

# Stage 2: production environment
FROM python:3.9.2-alpine3.13

WORKDIR /app
COPY --from=builder /wheels /wheels
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Expose port and run the application
EXPOSE 8081/TCP
CMD [ "python", "-u", "api.py" ]
