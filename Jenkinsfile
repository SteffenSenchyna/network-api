#!/usr/bin/env groovy

pipeline {
  environment {
    CHART_VER = sh(script: "helm show chart ./helm-chart | grep '^version:' | awk '{print \$2}'", returnStdout: true).trim()
    BUILD_VER = "1.0.0"
    GIT_COMMIT = sh(returnStdout: true, script: 'git rev-parse --short HEAD').trim()
    USER="ssenchyna"
    SERVICE = env.JOB_NAME.substring(0, env.JOB_NAME.lastIndexOf('/'))
    CHART_CHANGE="false"
    NETBOXTOKEN="123"
    NETBOXURL="0.0.0.0"
    DISCORDURL=""
    AWS_ACCESS_KEY=""
    AWS_SECRET_KEY=""
    AWS_DEFAULT_REGION=""
    AWS_S3_BUCKET_NAME=""
    NETWORKAPIURL=""
    MONGOURL=""  
    }

  agent any

  stages {   
      stage("Docker login") {
        steps {
          sh """
            ## Login to Docker Repo ##
            echo ${env.DOCKER_PASS} | docker login -u $USER --password-stdin
            echo ${env.DOCKER_PASS} | helm registry login registry-1.docker.io -u $USER --password-stdin 
          """
        }
      }

      stage("Clone Cluster Chart Repo") {
        steps {
          // Clone the Git repository
          sh """
          git clone https://github.com/SteffenSenchyna/cluster-chart.git
          """
          // Check to see if there where any changes made to the helm chart
          sh("ls")
          script {
            def CHART_VER_DEV = sh(script: "helm show chart ./cluster-chart/dev/ | grep '^version:' | awk '{print \$2}'", returnStdout: true).trim()
            if (CHART_VER_DEV != CHART_VER) {
                env.CHART_CHANGE = "true"
            } 
          }
          sh('echo "Hit"')
        }
      }

      stage("Build/Push Docker Image") {
          steps {
              sh """
              docker build -t ${env.DOCKER_REPO}/$SERVICE:$BUILD_VER-$GIT_COMMIT .
              docker push ${env.DOCKER_REPO}/$SERVICE:$BUILD_VER-$GIT_COMMIT
              // yq e --arg service "$SERVICE" --arg tag "$BUILD_VER-$GIT_COMMIT" '.[$service].image.tag = $tag' ./cluster-chart/dev/$SERVICE/values.yaml
              """
          }
      }

      stage("Build/Push Helm Chart") {
        when {
            // Execute the stage only if the remote chart version is different from the current chart version
            expression { env.CHART_CHANGE != "true" }
        }
        steps {
            sh """
            sed -i 's/version:.*/version: $BUILD_VER-$GIT_COMMIT/' ./cluster-chart/dev/$SERVICE/Chart.yaml
            helm package ./helm-chart
            helm push "$SERVICE-$CHART_VER".tgz oci://registry-1.docker.io/$USER
            """
          }
      }

      stage("Commit Changes to Cluster Chart Repo") {
        steps {
            sh """
            cd cluster-chart
            git add .
            """
            script {
                def commitMsg
                sh "git diff --name-only HEAD | sort | uniq > changed_files.txt"
                def changedFiles = readFile('changed_files.txt').trim()
                if (changedFiles.contains('values.yaml') && changedFiles.contains('Chart.yaml')) {
                    commitMsg = "change the ${SERVICE} image tag to ${BUILD_VER}-${GIT_COMMIT} and the chart version to ${CHART_VER}"
                } else if (changedFiles.contains('values.yaml')) {
                    commitMsg = "change the image tag to ${VAR}"
                } else {
                    commitMsg = "No relevant changes to chart values found"
                }
                sh """
                git commit -m "${commitMsg}"
                git push
                """
            }
        }     
      }
    }
    // Clean up 
    post {
    always {
        sh 'rm *.tgz'
        sh 'rm -r cluster-chart'
    }
  }
}