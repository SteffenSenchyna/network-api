import os

# Define the image name and tag
image_name = 'ssenchyna/network-api'
image_tag = 'latest'

# Build the Docker image
os.system(f'docker build -t {image_name}:{image_tag} .')

# Log in to Docker Hub
os.system('docker login')

# Push the Docker image to Docker Hub
os.system(f'docker push {image_name}:{image_tag}')
