pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh '''#!/bin/bash
            python3.9 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            pip install gunicorn pymysql cryptography
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
            pytest --junit-xml=test-reports/results.xml ./tests/units/ --verbose
            '''
        }
        post {
            always {
            junit 'test-reports/results.xml'
            }
        }
    }
    stage ('OWASP FS SCAN') {
      steps {
        dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
        dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
      }
    }
    stage ('Clean') {
      steps {
        sh '''#!/bin/bash
            if [[ $(ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2) != 0 ]]
            then
              ps aux | grep -i "gunicorn" | tr -s " " | head -n 1 | cut -d " " -f 2 > pid.txt
              kill $(cat pid.txt)
              exit 0
            fi
        '''
      }
    }
    stage('Deploy') {
      steps {
        sh '''#!/bin/bash
            source venv/bin/activate
            nohup gunicorn -b :5000 -w 4 microblog:app &
        '''
      }
    }
  }
}
