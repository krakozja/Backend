def imageName="krakozja/backend"
def dockerTag=""
def dockerRegistry=""
def registryCredentials="dockerhub"

pipeline {
    agent {
        label 'agent'
    }

    environment {
        scannerHome = tool 'SonarQube'
        PIP_BREAK_SYSTEM_PACKAGES = 1
    }

    stages {
        stage('Get Code') {
            steps {
                checkout scm // Get some code from a GitHub repository
            }
        }

        stage('Unit tests') {
            steps {
                sh "pip3 install -r requirements.txt"
                sh "python3 -m pytest --cov=. --cov-report xml:test-results/coverage.xml --junitxml=test-results/pytest-report.xml"
            }
        }

        stage('Sonarqube analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }

        stage('Build application image') {
            steps {
                script {
                  // Prepare basic image for application
                  dockerTag = "RC-${env.BUILD_ID}.${env.GIT_COMMIT.take(7)}"
                  applicationImage = docker.build("$imageName:$dockerTag",".")
                }
            }
        }

        stage ('Pushing image to docker registry') {
            steps {
                script {
                    docker.withRegistry("$dockerRegistry", "$registryCredentials") {
                        applicationImage.push()
                        applicationImage.push('latest')
                    }
                }
            }
        }

        stage ('Push to Repo') {
            steps {
                dir('ArgoCD') {
                    withCredentials([gitUsernamePassword(credentialsId: 'git', gitToolName: 'Default')]) {
                        git branch: 'main', url: 'https://github.com/krakozja/ArgoCD.git'
                        sh """ cd backend
                        sed -i "s#$imageName.*#$imageName:$dockerTag#g" deployment.yaml
                        git commit -am "Set new $dockerTag tag."
                        git push origin main
                        """
                    }
                }
            }
        }
    }
    post {
        always {
            junit testResults: "test-results/*.xml"
            cleanWs()
        }
        success {
            build job: 'app_of_apps', parameters: [ string(name: 'frontendDockerTag', value: "$dockerTag")], wait: false
        }
    }
}
