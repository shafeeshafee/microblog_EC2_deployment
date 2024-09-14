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
        // stage('OWASP FS SCAN') {
        //     steps {
        //         sh '''#!/bin/bash
        //         /var/lib/jenkins/tools/org.jenkinsci.plugins.DependencyCheck.tools.DependencyCheckInstallation/DP-Check/bin/dependency-check.sh --scan ./ --disableYarnAudit --disableNodeAudit
        //         '''
        //         dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
        //     }
        // }
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
                # Activate the virtual environment
                source venv/bin/activate
                
                # Ensure gunicorn is installed within the venv
                if ! pip show gunicorn > /dev/null 2>&1; then
                    echo "Gunicorn is not installed in the virtual environment. Installing..."
                    pip install gunicorn
                fi
                
                # Check if gunicorn is already running
                if pgrep -f "gunicorn"; then
                    echo "Gunicorn is already running. Skipping start."
                else
                    echo "Gunicorn is not running. Starting gunicorn..."
                    nohup gunicorn -b :5000 -w 4 microblog:app > gunicorn.log 2>&1 &
                fi
                '''
            }
        }
    }
}
