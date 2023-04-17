FROM python:3.9.2-alpine3.13 
# To build container run 
# docker build -t ssenchyna/network-api-docker . && docker push ssenchyna/network-api-docker
# We copy just the requirements.txt first to leverage Docker cache
RUN pip install --upgrade pip
RUN pip install --upgrade wheel setuptools
RUN apk upgrade
RUN apk add --update gcc musl-dev libffi-dev libressl-dev
COPY . /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt 
EXPOSE 8081/TCP
CMD [ "python", "-u", "api.py" ]