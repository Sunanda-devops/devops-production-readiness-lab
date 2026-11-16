pipeline {
    agent any

    environment {
        IMAGE = "production-readiness-api:${env.GIT_COMMIT}"
    }

    stages {
        stage('Test') {
            steps {
                sh 'python3 -m venv .venv-ci'
                sh '. .venv-ci/bin/activate && pip install -r requirements-dev.txt && pytest -q'
            }
        }
        stage('Quality and security') {
            steps {
                sh '. .venv-ci/bin/activate && ruff check . && bandit -r app -ll'
                sh 'gitleaks detect --source . --no-banner'
            }
        }
        stage('Build and scan') {
            steps {
                sh 'docker build --tag "$IMAGE" .'
                sh 'trivy image --scanners vuln,secret,misconfig --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 "$IMAGE"'
            }
        }
    }

    post {
        always {
            sh 'rm -rf .venv-ci'
        }
    }
}
