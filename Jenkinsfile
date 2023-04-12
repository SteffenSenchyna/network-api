#!/usr/bin/env groovy

pipeline {
  environment {
    USER="ssenchyna"
    BUILDER_NAME='mbuilder'
    SERVICE="network-api"
    NETBOXTOKEN="0123456789abcdef0123456789abcdef01234567"
    NETBOXURL="0.0.0.0:8000"
    DISCORDURL="https://discord.com/api/webhooks/1091090100760354907/BitSvRvkRg7j9x2nusu5z1x2fauMxvXWmTE0yh8_xrrN5EDYpwrLbUemYXkqqA8iLlDI"
  }

  agent any

  stages {

    stage('Build For Unit Testing') {
        steps {
          sh 'pip install -r requirements.txt'
        }
      }

    stage ('Unit Testing'){
        steps {
        sh 'python3 -m unittest discover -s tests -p "*_test.py"'
        }
      }
    
    stage("Docker login") {
      steps {
        sh """
          ## Login to Docker Repo ##
          echo ${env.DOCKER_PASS} | docker login -u $USER --password-stdin 
        """
      }
    }

    //Note: qemu is responsible for building images that are not supported by host
    stage("Register QEMU emulators") {
      steps {
        sh """
        docker run --rm --privileged docker/binfmt:820fdd95a9972a5308930a2bdfb8573dd4447ad3
        cat /proc/sys/fs/binfmt_misc/qemu-aarch64
        """
      }
    }

    //Create a buildx builder container to do the multi-architectural builds
    stage("Create Buildx Builder") {
      steps {
        sh """
          ## Create buildx builder
          docker buildx create --name dev-$BUILDER_NAME
          docker buildx use $BUILDER_NAME
          docker buildx inspect --bootstrap

          ## Sanity check step
          docker buildx ls
        """
      }
    }

    //Build using buildx
    stage("Build multi-arch image") {
        steps {
            sh """
                docker buildx build --platform linux/amd64, linux/arm64 --push -t ${env.DOCKER_REPO}/$SERVICE:${env.BUILD_NUMBER} . 
                """
        }
    }

    // Cleaning up
    stage("Destroy buildx builder") {
      steps {
        sh """
          docker buildx use default docker buildx rm $BUILDER_NAME

          ## Sanity check step
          docker buildx ls
          """
      }
    }
  }
}