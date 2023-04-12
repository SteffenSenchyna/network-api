#!/usr/bin/env groovy

pipeline {
  environment {
    USER="ssenchyna"
    PASSWORD=$DOCKER_PASSWORD
    DOCKER_REGISTRY=$DOCKER_REPO
    BUILDER_NAME='mbuilder'
    SERVICE="network-api"
  }

  agent any

  stages {

    stage("Docker login") {
      steps {
        sh """
          ## Login to Docker Repo ##
          docker login -u $USER -p $PASSWORD $DOCKER_REGISTRY 
        """
      }
    }

    // Note: qemu is responsible for building images that are not supported by host
    stage("Register QEMU emulators") {
      steps {
        sh """
        docker run --rm --privileged docker/binfmt:820fdd95a9972a5308930a2bdfb8573dd4447ad3
        cat /proc/sys/fs/binfmt_misc/qemu-aarch64
        """
      }
    }

    // Create a buildx builder container to do the multi-architectural builds
    stage("Create Buildx Builder") {
      steps {
        sh """
          ## Create buildx builder
          docker buildx create --name $BUILDER_NAME
          docker buildx use $BUILDER_NAME
          docker buildx inspect --bootstrap

          ## Sanity check step
          docker buildx ls
        """
      }
    }

    // Now we build using buildx
    stage("Build multi-arch image") {
        steps {
            sh """
                docker buildx build --platform linux/amd64,linux/arm64 --push -t $DOCKER_REGISTRY/$SERVICE:$TAG .
            """
        }
    }

    // Need to clean up
    stage("Destroy buildx builder") {
      steps {
        sh """
          docker buildx use default
          docker buildx rm $BUILDER_NAME

          ## Sanity check step
          docker buildx ls
        """
      }
    }
}}