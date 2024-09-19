pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh '''#!/bin/bash
                if [ ! -d "venv" ]; then
                    python3.9 -m venv venv
                fi
                source venv/bin/activate
                pip install -r requirements.txt
                export FLASK_APP=microblog.py
                flask db upgrade
                flask translate compile
                '''
            }
        }
        stage('Test') {
            steps {
                sh '''#!/bin/bash
                source venv/bin/activate
                export PYTHONPATH=$PYTHONPATH:$(pwd)
                export FLASK_APP=microblog.py
                pytest --junit-xml=test-reports/results.xml ./tests/units/ --verbose
                '''
            }
            post {
                always {
                    junit 'test-reports/results.xml'
                }
            }
        }
        stage('OWASP FS SCAN') {
            steps {
                withCredentials([string(credentialsId: 'NVD_API_KEY', variable: 'NVD_API_KEY')]) {
                    dependencyCheck additionalArguments: "--scan ./ --disableYarnAudit --disableNodeAudit --nvdApiKey ${NVD_API_KEY}", odcInstallation: 'DP-Check'
                    dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
                }
            }
        }
        stage('Clean') {
            steps {
                sh '''#!/bin/bash
                PID=$(pgrep gunicorn)
                if [ -n "$PID" ]; then
                    kill $PID
                    echo "Killed gunicorn process with PID: $PID"
                else
                    echo "No gunicorn process running"
                fi
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''#!/bin/bash
                set -x  # Enable command echoing for debugging
                
                echo "Attempting to restart microblog service..."
                if sudo /bin/systemctl restart microblog; then
                    echo "Microblog service restarted successfully"
                else
                    echo "Failed to restart microblog service"
                    sudo /bin/systemctl status microblog || true
                    exit 1
                fi
                
                echo "Waiting for service to stabilize..."
                sleep 10
                
                echo "Checking service status..."
                if sudo /bin/systemctl is-active microblog; then
                    echo "Microblog service is active"
                    sudo /bin/systemctl status microblog || true
                else
                    echo "Microblog service failed to start"
                    sudo /bin/systemctl status microblog || true
                    exit 1
                fi
                '''
            }
        }
    }
}