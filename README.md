# AWS Self-Healing Application Monitoring System

A hands-on DevOps project that monitors Apache HTTPD running on AWS EC2 instances and automatically attempts to recover the service when it goes down.

## Project Overview

I built a Python monitoring agent using Boto3 to check the Apache HTTPD service running on application EC2 instances.

If Apache is detected as stopped, the agent uses AWS Systems Manager (SSM) to send a command to start the service again.

The system was tested by intentionally stopping Apache and observing the recovery process.

## Technologies Used

- AWS EC2
- AWS Systems Manager (SSM)
- AWS IAM
- Application Load Balancer
- Target Groups
- Linux
- Apache HTTPD
- Python
- Boto3
- Docker

## How It Works

```text
User
  ↓
Application Load Balancer
  ↓
Target Group
  ↓
EC2 Application Servers
  ↓
Apache HTTPD

Monitoring EC2
  ↓
Python + Boto3
  ↓
AWS Systems Manager (SSM)
  ↓
Checks Apache HTTPD
  ↓
If Apache is DOWN
  ↓
SSM sends recovery command
  ↓
systemctl start httpd
  ↓
Apache starts again


## Architecture

The project consists of two main parts:

- **Application Layer:** Application Load Balancer distributes traffic to two EC2 instances running Apache HTTPD.
- **Monitoring Layer:** A separate EC2 instance runs the Python/Boto3 monitoring agent. It uses AWS Systems Manager (SSM) to check and recover the Apache service.

> Architecture diagram will be added here.


## Failure and Recovery Flow

```text
 Apache is healthy
        ↓
 Apache HTTPD is intentionally stopped
        ↓
 Monitoring agent detects "inactive"
        ↓
 Failure is logged
        ↓
 Boto3 sends recovery request to AWS SSM
        ↓
 SSM executes:
   systemctl start httpd
        ↓
 Apache starts successfully
        ↓
 Application service is recovered 


 ## Project Structure

```text
aws-self-healing-monitoring/
│
├── architecture/
│
├── screenshots/
│   ├── 1.ai-healing-ec2.PNG
│   ├── 2.ai-agent-Lb.PNG
│   ├── 3.ai-agent-target-grp.PNG
│   ├── 4.ai-healing-iamrole.PNG
│   ├── ai-agent-ec2-2.PNG
│   ├── ai-agent-ec21.PNG
│   ├── ai-healing-ec2active check.PNG
│   ├── ai-healing-ec2inactive check.PNG
│   ├── ai-healing-log check1.PNG
│   └── ai-healing-logcheck2.PNG
│
├── src/
│   ├── agent-os.py
│   ├── dockerfile
│   └── requirements.txt
│
└── README.md



## How I Built It

1. Created two EC2 instances to run the Apache HTTPD application.
2. Created an Application Load Balancer and Target Group to distribute traffic between the application servers.
3. Created a separate EC2 instance for the monitoring agent.
4. Developed a Python monitoring agent using Boto3.
5. Configured IAM permissions required for the monitoring agent to communicate with the application instances through AWS Systems Manager (SSM).
6. Containerized the monitoring agent using Docker.
7. The agent periodically checks the Apache HTTPD service.
8. If Apache is detected as inactive, the agent sends a recovery command through SSM.
9. Tested the self-healing behavior by intentionally stopping Apache and observing its recovery.


## Challenges Faced

During the implementation, I faced IAM permission issues while trying to execute commands on the application EC2 instances through AWS Systems Manager (SSM).

I investigated the required permissions, updated the IAM role with the necessary SSM-related policies, and tested the communication again until the monitoring and recovery process worked successfully.