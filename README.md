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
* 📆 Lightweight SQLite bac
