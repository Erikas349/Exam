# 📝 To-Do Application - Exam Project

A full-stack To-Do application with automated CI/CD, AWS deployment using Terraform, container orchestration via Docker Compose, and observability using Prometheus and Grafana.

---

## 📌 Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Features](#features)
4. [Tech Stack](#tech-stack)
5. [Local Development Setup](#local-development-setup)
6. [Infrastructure as Code (Terraform)](#infrastructure-as-code-terraform)
7. [CI/CD Pipeline](#cicd-pipeline)
8. [Monitoring & Observability](#monitoring--observability)
9. [Security Considerations](#security-considerations)
10. [Future Enhancements](#future-enhancements)
11. [Author](#author)

---

## 📘 Project Overview

This application allows users to manage personal tasks using a simple interface backed by a RESTful API. It is designed to demonstrate DevOps practices such as:

* Infrastructure provisioning via Terraform.
* CI/CD with GitHub Actions.
* Containerization using Docker.
* Observability using Prometheus and Grafana.
* Deployment on AWS EC2 (free-tier compatible).

---

## 📺 Architecture Diagram

```
+------------+       +---------------+       +-----------------+
|  Frontend  | <---> |   Flask API   | <-->  |     SQLite DB    |
|  (React)   |       |  (Backend)    |       | (Local Database) |
+------------+       +---------------+       +-----------------+

     |                      |                            |
     v                      v                            v
+----------+       +------------------+        +-----------------+
| Grafana  | <---  |   Prometheus     | <----- | Flask Metrics   |
+----------+       +------------------+        +-----------------+

Infrastructure Provisioned with Terraform --> AWS EC2 (Ubuntu)
CI/CD --> GitHub Actions + SSH Deploy
```

---

## ✨ Features

* ✅ Task creation, deletion, updating
* 📆 Lightweight SQLite backend for local development
* 🌐 REST API with CORS enabled
* 🐳 Multi-container Dockerized environment
* 📈 Real-time metrics monitoring with Grafana dashboards
* ⭮️ CI/CD using GitHub Actions + SSH to AWS
* ☁️ Infrastructure provisioning via Terraform (EC2 + security groups)

---

## 🔧 Tech Stack

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Frontend         | React, Axios           |
| Backend          | Flask, Flask-CORS      |
| Database         | SQLite                 |
| CI/CD            | GitHub Actions         |
| Infrastructure   | Terraform (AWS EC2)    |
| Containerization | Docker, Docker Compose |
| Monitoring       | Prometheus, Grafana    |

---

## 💻 Local Development Setup

### Prerequisites

* Docker + Docker Compose
* Git
* Python 3 (for backend development)
* Node.js & npm (for frontend development)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Erikas349/Exam.git
cd Exam/To-Do-app
```

### Step 2: Run Using Docker Compose

```bash
docker-compose up --build
```

### Default Ports

| Service     | URL                                            |
| ----------- | ---------------------------------------------- |
| Frontend    | [http://localhost:3000](http://localhost:3000) |
| Backend API | [http://localhost:5000](http://localhost:5000) |
| Prometheus  | [http://localhost:9090](http://localhost:9090) |
| Grafana     | [http://localhost:3001](http://localhost:3001) |

---

## 🌍 Infrastructure as Code (Terraform)

Navigate to the Terraform folder:

```bash
cd ../terraform
```

### Steps to Deploy:

1. Initialize Terraform:

```bash
terraform init
```

2. Review the plan:

```bash
terraform plan
```

3. Apply changes:

```bash
terraform apply
```

### Resources Created:

* AWS EC2 instance (Ubuntu)
* Security group allowing:

  * Port 22 (SSH)
  * Port 80/3000 (HTTP frontend)
  * Port 5000 (Backend)
  * Port 9090/3001 (Monitoring)

---

## 🔄 CI/CD Pipeline

Defined in `.github/workflows/deploy.yml`.

### Trigger:

* On `push` or `pull_request` to the `main` branch

### Actions Performed:

* ✅ Install dependencies
* 🔍 Run backend/frontend tests (optional)
* 🐳 Build Docker images
* 🚀 SSH into EC2 and deploy latest version

### Required Secrets:

| Secret Name    | Description                                 |
| -------------- | ------------------------------------------- |
| `AWS_HOST`     | Public IP or DNS of your EC2 instance       |
| `AWS_USERNAME` | Default user (e.g., `ubuntu`)               |
| `AWS_SSH_KEY`  | Private key content for SSH (in PEM format) |

---

## 📊 Monitoring & Observability

### Prometheus

* Scrapes `/metrics` endpoint exposed by Flask
* Uses `prometheus.yml` for job config

### Grafana

* Dashboards automatically provisioned
* Default login: `admin` / `admin`
* Add Prometheus as a data source on startup

### Metrics Exposed

* Number of tasks
* Request count by endpoint
* Error rate
* Response times

---

## 🔐 Security Considerations

* SSH access limited to specified IPs in Terraform security group
* Sensitive keys stored as GitHub secrets
* Flask CORS configured to allow frontend access only
* SQLite used only for demo (not production-grade)

---

## 🔮 Future Enhancements

* Switch to PostgreSQL or AWS RDS
* HTTPS setup with Nginx + Let's Encrypt
* Backend and frontend tests with coverage reports
* Alerting with Grafana
* Use AWS S3 for storing frontend assets
* Auto-scaling setup with Terraform + Load Balancer

---

## 👤 Author

* **Name**: Erikas
* **GitHub**: [@Erikas349](https://github.com/Erikas349)
* **Exam Project**: Built with DevOps best practices in mind
