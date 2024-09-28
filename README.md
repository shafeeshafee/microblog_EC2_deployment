# Microblog EC2 Deployment

## Purpose

The goal of this workload is to deploy a social media application to servers on AWS EC2 instances, all via self-provisioning, instead of relying on managed services like AWS Elastic Beanstalk.

It involves setting up a continuous CI/CD pipeline using Jenkins, automating the build, testing, running security scans, and deployment processes, and implementing monitoring using Prometheus and Grafana to observe application and server resources. By provisioning our own infrastructure, we gain a deeper understanding of the deployment process, with the added ability to customize the environment to our specific needs, as well as enhance our knowledge of server management and application deployment pipelines.

![System Diagram](./diagram.png)

## Documenting Steps

1. **Set Up Jenkins**

   - Cloned the GitHub repository to our own account and created an Ubuntu EC2 instance named "Jenkins," installing Jenkins using an automated bash script. Cloning the repository provides control over the codebase. Automating the Jenkins installation ensures consistency and speeds up the setup of the CI/CD orchestrator.

2. **Configured the Server Environment**

   - Installed `python3.9`, `python3.9-venv`, `python3-pip`, and `nginx` by adding the Deadsnakes PPA to the server's package sources. These installations prepare the server with the necessary tools to run the Python application and serve it via Nginx.

3. **Set Up the Application in a Virtual Environment**

   - Cloned the application code onto the server, created a Python virtual environment, activated it, and installed all dependencies, including `gunicorn`, `pymysql`, and `cryptography`. Using a virtual environment isolates the application's dependencies, ensuring consistency and preventing conflicts with system packages.

4. **Configured Application Settings and Database**

   - Set the environment variable `FLASK_APP=microblog.py`, ran `flask translate compile` to prepare translations, and executed `flask db upgrade` to set up the database schema. These steps configured the application for deployment, ensuring language support and database migrations are up to date.

5. **Configured Nginx as a Reverse Proxy**

   - Edited the Nginx configuration to proxy requests from port 80 to the application running on port 5000. **Why Nginx?** Nginx handles client HTTP requests, improves security, and efficiently serves the application by forwarding requests to the Gunicorn server.

6. **Tested the Application Manually**

   - Started the application using `gunicorn -b :5000 -w 4 microblog:app` and accessed it in the browser to confirm it was running. Ensuring the application runs correctly in a manual setup verifies that the environment is properly configured before automating the deployment.

---

**Note:** Were the above steps involving setting up the Python virtual environment, installing dependencies, configuring environment variables, preparing the application for deployment, configuring Nginx, and launching with Gunicorn absolutely necessary for the CI/CD pipeline?

**Short Answer:** _No._

**Long Answer:** While these steps were useful for initially configuring and testing the application manually, they are not strictly necessary when using a CI/CD pipeline. Instead, the primary purpose of these steps is to ensure that the application can run locally before automating it within the pipeline's build and deploy stages to ensure consistency and repeatability. Automating these processes reduces the potential for manual errors and aligns with the principles of continuous integration and deployment.

---

7. **Automated the Pipeline with Jenkins**

   - Edited the `Jenkinsfile` to automate the build, test, and deploy stages, including commands to set up the environment, install dependencies, run tests, and deploy the application. Automating these steps in the CI/CD pipeline ensures consistent deployments and reduces manual errors.

8. **Implemented Unit Testing**

   - Created a unit test script `test_app.py` in the `tests/unit/` directory to test application functionality and included the test execution in the Jenkins pipeline. Automated testing catches issues early, maintaining code quality and reliability.

9. **OWASP Scanning**

   - Obtained an OWASP API Key to scan the project's dependencies.

   **Summary of Results Found in `dependency-check-report.xml` in My Workspace:**

   | File Name     | File Path                                              | SHA-256 Hash (Truncated)  | Vulnerability ID                             | Confidence |
   | ------------- | ------------------------------------------------------ | ------------------------- | -------------------------------------------- | ---------- |
   | cli-32.exe    | /var/lib/jenkins/.../setuptools/cli-32.exe             | 32acc1bc543116cbe2cff...  | cpe:2.3:a:cli\*project:cli:32:_:*:*:*:*:\_:_ | HIGH       |
   | cli-64.exe    | /var/lib/jenkins/.../setuptools/cli-64.exe             | bbb3de5707629e6a60a0c...  | cpe:2.3:a:cli\*project:cli:64:_:*:*:*:*:\_:_ | HIGH       |
   | debugger.js   | /var/lib/jenkins/.../werkzeug/debug/shared/debugger.js | 155041522af3e2429e748...  | None identified                              | N/A        |
   | gui-32.exe    | /var/lib/jenkins/.../setuptools/gui-32.exe             | 85dae1e95d77845f2cb59...  | None identified                              | N/A        |
   | gui-64.exe    | /var/lib/jenkins/.../setuptools/gui-64.exe             | 3471b6140eadc6412277d...  | None identified                              | N/A        |
   | gui-arm64.exe | /var/lib/jenkins/.../setuptools/gui-arm64.exe          | e694f4743405c8b5926ff...  | None identified                              | N/A        |
   | t32.exe       | /var/lib/jenkins/.../pip/\_vendor/distlib/t32.exe      | 6b4195e640a85ac32eb6f...  | None identified                              | N/A        |
   | t64-arm.exe   | /var/lib/jenkins/.../pip/\_vendor/distlib/t64-arm.exe  | ebc4c06b7d95e74e315419... | None identified                              | N/A        |
   | t64.exe       | /var/lib/jenkins/.../pip/\_vendor/distlib/t64.exe      | 81a618f21cb87db9076134... | None identified                              | N/A        |
   | w32.exe       | /var/lib/jenkins/.../pip/\_vendor/distlib/w32.exe      | 47872cc77f8e18cf642f8...  | None identified                              | N/A        |
   | w64-arm.exe   | /var/lib/jenkins/.../pip/\_vendor/distlib/w64-arm.exe  | c5dc9884a8f458371550e...  | None identified                              | N/A        |
   | w64.exe       | /var/lib/jenkins/.../pip/\_vendor/distlib/w64.exe      | 7a319ffaba23a017d7b1e...  | None identified                              | N/A        |

10. **Set Up Continuous Deployment and Service Management**

    - Created a `systemd` service for the application to manage it as a background process, modified the Jenkins deploy stage to restart the service, and adjusted permissions to allow Jenkins to manage the service without requiring a password. Managing the application as a service ensures it runs continuously and restarts automatically, while automation in the pipeline enhances efficiency.

    With this step, we can finally see our website running upon successful Jenkins build updates.

    ![Website Screenshot, Microblog Site](./screenshot_1.png)

11. **Installing the Node Exporter on Jenkins Server**

    - **Issue:** Needed system metrics collection for monitoring Jenkins.
    - **Solution:** Installed Prometheus Node Exporter on the Jenkins server, configured it as a `systemd` service, allowed necessary firewall ports, and enabled the service to run on startup.

    ![Node Exporter](./screenshot_4.png)

12. **Implemented Monitoring with Prometheus and Grafana**

    - Set up a new EC2 instance named "Monitoring," installed Prometheus and Grafana, configured them to collect metrics from the Jenkins server and application, and set up dashboards for visualization. Monitoring provides insights into application performance and server health, allowing for proactive issue detection and resource management.

    ### Endpoint Targets We're Scraping with Prometheus

    ![Prometheus Dashboard](./screenshot_2.png)

    ### Example Visualization with Grafana Pulling from Prometheus

    ![Grafana Dashboard](./screenshot_grafana.png)
    ![Grafana Dashboard 2](./screenshot_grafana_2.png)

---

## Issues/Troubleshooting

1. **Installing Python 3.9**

   - **Issue:** Unable to locate package `python3.9` in the default Ubuntu repositories.
   - **Solution:** Added the Deadsnakes PPA to access Python 3.9 packages.

2. **Jenkins Slowness**

   - **Issue:** Jenkins was slow due to IP configuration issues.
   - **Solution:** Updated the Jenkins configuration file (`/var/lib/jenkins/jenkins.model.JenkinsLocationConfiguration.xml`) with the latest server IP and restarted Jenkins.

3. **Dependency-Check Plugin Delay**

   - **Issue:** The OWASP Dependency-Check plugin took excessive time due to a missing NVD API key.
   - **Solutions:**
     - Temporarily commented out the OWASP scan in the `Jenkinsfile` to allow the pipeline to proceed. Noted the need to obtain an NVD API key to speed up future scans.
     - Obtained the API key, added it to Jenkins credentials, performed a scan, and resolved the issue.

4. **Jenkinsfile Errors**

   - **Issue:** Encountered errors in the `Jenkinsfile`, such as incorrect commands and path issues.
   - **Solution:** Corrected syntax errors, ensured the virtual environment was activated in each stage, granted Jenkins the ability to run `systemd` commands for `microblog`, and adjusted file paths.

5. **ModuleNotFoundError During Testing**

   - **Issue:** Tests failed with `ModuleNotFoundError: No module named 'microblog'`.
   - **Solution:** Set the `PYTHONPATH` environment variable to the project's root directory to ensure Python could locate the modules.

6. **Gunicorn Worker Count**

   - **Issue:** The `t3.micro` instance couldn't handle 4 Gunicorn workers, causing high CPU usage and freezing.
   - **Solution:** Switched to a `t3.medium` instance.

7. **OWASP Dependency-Check Plugin Slowness**

   - **Issue:** The OWASP scan took a very long time or caused the instance to crash due to resource constraints and API rate limiting.
   - **Solutions:**
     - Obtained an NVD API key to reduce rate limiting issues.
     - Considered increasing the EC2 instance size to handle resource demands.

8. **Reassessing the Clean Stage**

   - **Issue:** The Clean stage in the `Jenkinsfile` attempted to kill Gunicorn processes but failed due to permission issues and only killed one of the child workers but not the main process.
   - **Solution:** Recognized that managing Gunicorn via `systemd` negates the need for this stage (refer to Issue #9) and considered removing or modifying it accordingly. Used `systemctl` to restart the process.

9. **Background Processes Terminating**

   - **Issue:** The application process terminated when the pipeline completed.
   - **Solution:** Created a `systemd` service to manage the Gunicorn process, ensuring it runs continuously in the background.
     - With `systemd`, whenever you add something, you must reload the daemon, enable the service, start it, and check the status:
       ```bash
       sudo systemctl daemon-reload
       sudo systemctl enable microblog
       sudo systemctl start microblog
       sudo systemctl status microblog
       ```

10. **IP Address Changes**

    - **Issue:** EC2 instance IP addresses changed after stopping and starting, causing connection issues.
    - **Solution:** Reconfigured applications with the new IP addresses. Recognized that using Elastic IPs could prevent this issue but did not implement them for this workload.

11. **Monitoring Setup Challenges**

    - **Issue:** Difficulty setting up Prometheus to scrape metrics from the Jenkins server.
    - **Solution:** Installed `Node Exporter` on the Jenkins server, adjusted security group settings, and updated Prometheus configuration to include the Jenkins server as a target.

## Optimization

### The Power of Provisioning It Ourselves

Provisioning our own infrastructure instead of relying on managed services like AWS Elastic Beanstalk offers several key benefits:

- **Complete Control:** Self-provisioning grants full control over every aspect of the infrastructure. This allows for tailored configurations to meet specific application needs, such as selecting exact instance types, customizing network settings, and installing required software without the limitations imposed by managed services.
- **Cost Optimization:** By managing resources directly, there is potential to optimize costs. We pay only for the resources we use and can fine-tune our infrastructure to prevent over-provisioning, which is sometimes unavoidable with managed services.
- **Comprehensive Understanding:** Building and managing the infrastructure ourselves, although cumbersome at times, enhances our understanding of underlying components like server setup, networking, security configurations, and deployment pipelines, which is essential for tackling more complex projects in the future.

### Is This a "Good System"?

Assessing the quality of this system involves weighing its strengths against its weaknesses:

**Strengths:**

- The system effectively deploys the application using a CI/CD pipeline with Jenkins, incorporates automated testing, and sets up monitoring with Prometheus and Grafana.
- The process offers a comprehensive learning experience in setting up and managing infrastructure manually, which helps us understand the deployment processes and tools.

**Weaknesses:**

- Manual server provisioning and configuration introduce complexities and are time-consuming. This approach increases the risk of human error and makes scaling difficult.
- The current setup lacks mechanisms for automatic scaling to handle variable workloads, which could lead to performance issues under high traffic.
- Without granular security measures, manually managed infrastructure can be vulnerable to misconfigurations and unauthorized access.
- **Resource Contention:** Hosting both Jenkins and the application on the same EC2 instance can lead to resource contention, affecting the performance and reliability of both services.

While the system serves its purpose and provides valuable hands-on experience, it falls short of being a "good system" in a production context. It lacks scalability, comprehensive security, and efficient resource management, which are essential traits of a production-grade environment.

### Optimizations / Future Deployments

1. **Implement Infrastructure as Code (IaC):**

   - Use tools like **Terraform** or **AWS CloudFormation** to automate and manage the infrastructure.
   - **Why?** IaC promotes consistency across environments, reduces manual errors, and allows for version control of infrastructure configurations. It makes scaling and replicating environments more straightforward.

2. **Separate Jenkins and Application Servers:**

   - Deploy Jenkins and the application on separate EC2 instances. This separation prevents resource contention, ensuring that CI/CD processes do not impact application performance. It enhances reliability and allows each service to scale independently.

3. **Utilize Elastic IPs:**

   - Assign Elastic IPs to EC2 instances to maintain consistent public IP addresses. This prevents connectivity issues caused by IP address changes when instances are stopped and started, improving reliability and simplifying configuration.

4. **Set Up a Custom Virtual Private Cloud (VPC):**

   - Create a custom VPC with public and private subnets, security groups, and network access control lists (ACLs).
   - **Why?** A custom VPC offers enhanced security and network control. It allows for the isolation of resources, better traffic management, and adherence to best practices in network architecture.

5. **Implement Auto Scaling and Load Balancing:**

   - Use Auto Scaling Groups and Elastic Load Balancers to manage application instances. Auto Scaling adjusts the number of running instances based on demand, providing high availability and optimal performance. Load balancing distributes incoming traffic evenly, preventing any single instance from becoming a bottleneck.

6. **Enhance Security Measures:**

   - Apply security best practices, including:
     - Configuring IAM roles with the principle of least privilege.
     - Tightening security group rules to allow only necessary traffic.
     - Regularly updating and patching servers.
     - Enforcing encryption for data at rest and in transit.
     - Implementing Multi-Factor Authentication (MFA) for critical operations.

7. **Containerization and Orchestration:**

   - Containerize the application using Docker and manage it with orchestration tools like Kubernetes.

8. **Automate Deployment Processes:**
   - Use CI/CD tools to automate the entire deployment pipeline, including testing, security scans, and deployment to production.
   - **Why?** Automation reduces manual intervention, minimizes errors, and optimizes the deployment cycle, allowing for more frequent and reliable releases.

## Conclusion

This workload provided practical experience in deploying a web application on self-provisioned EC2 instances, setting up a CI/CD pipeline with Jenkins, and implementing monitoring solutions with Prometheus and Grafana. It showcases the intricacies and considerations of managing infrastructure independently, emphasizing the importance of automation and monitoring. While provisioning our own resources offers more flexibility, it also requires diligent management to ensure reliability, security, and scalability are maintained.
