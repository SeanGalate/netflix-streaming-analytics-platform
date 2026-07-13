# Netflix Streaming Analytics Platform

## Project Overview

The **Netflix Streaming Analytics Platform** is a production-inspired data engineering project designed to simulate the architecture and workflows used by large-scale streaming platforms such as Netflix.

The goal is to build an end-to-end analytics platform capable of ingesting millions of streaming events, processing them through a modern lakehouse architecture, and producing both real-time and historical business insights.

This project is being developed incrementally and emphasizes production-ready engineering practices, including scalable data pipelines, cloud infrastructure, orchestration, observability, and performance optimization.

---

## Architecture

> **Architecture diagram coming soon**

<!-- Replace this section with a system architecture diagram as the project evolves. -->

---

## Tech Stack

### Programming Languages
- Python
- SQL

### Data Processing
- Apache Spark
- Databricks
- Delta Lake

### Workflow Orchestration
- Apache Airflow

### Cloud Platform
- Amazon Web Services (AWS)

### AWS Services
- Amazon S3
- AWS Glue Catalog
- Amazon Athena
- Amazon CloudWatch
- AWS IAM
- AWS Secrets Manager
- Amazon EC2

### Storage
- Delta Lake
- Apache Parquet

### Infrastructure
- Terraform

### Version Control
- Git
- GitHub

---

## Future Roadmap

### ✅ Phase 0 — Project Setup
- Create GitHub repository
- Establish project directory structure
- Create project documentation
- Make initial commits

### Phase 1 — Event Generator
- Build a realistic Netflix streaming event generator
- Simulate user activity (play, pause, stop, search, ratings, etc.)
- Generate raw JSON streaming events

### Phase 2 — Bronze Layer
- Ingest raw streaming events
- Store data in Delta Lake
- Implement schema enforcement
- Add ingestion timestamps and partitioning

### Phase 3 — Silver Layer
- Clean and validate data
- Remove duplicates and invalid records
- Standardize timestamps
- Enrich and transform streaming events

### Phase 4 — Gold Analytics
- Create business-ready analytics tables
- Compute KPIs such as DAU, MAU, watch time, retention, churn, and engagement metrics
- Support reporting and dashboarding

### Phase 5 — Airflow Orchestration
- Build production ETL workflows
- Schedule Spark jobs
- Implement retries, Task Groups, sensors, SLAs, and notifications
- Automate end-to-end pipeline execution

### Phase 6 — AWS Infrastructure
- Deploy the platform to AWS
- Configure Amazon S3 data lake
- Integrate Databricks
- Configure AWS Glue Catalog and Amazon Athena
- Provision infrastructure using Terraform

### Phase 7 — Monitoring & Observability
- Implement pipeline monitoring
- Track data freshness and record counts
- Configure CloudWatch dashboards and alerts
- Monitor Spark jobs and pipeline health

### Phase 8 — Performance Optimization
- Optimize Spark jobs
- Implement partition pruning and caching
- Use broadcast joins and Adaptive Query Execution (AQE)
- Optimize Delta Lake with Z-Ordering and compaction

### Phase 9 — Interview Notes & Resume Bullets
- Finalize project documentation
- Create architecture diagrams
- Record design decisions and lessons learned
- Prepare resume-ready accomplishments
- Create an end-to-end project demonstration and walkthrough

---

## Project Goals

By the completion of this project, the platform will demonstrate experience with:

- Designing scalable data architectures
- Building distributed Spark pipelines
- Implementing a Medallion (Bronze, Silver, Gold) architecture
- Working with Delta Lake
- Cloud-native data engineering on AWS
- Workflow orchestration with Apache Airflow
- Infrastructure as Code using Terraform
- Advanced SQL analytics
- Data quality and observability
- Performance optimization for large-scale data processing

---

## Project Status

**Status:** 🚧 In Development

This repository is a long-term portfolio project that will continue to evolve as new features, optimizations, and production engineering practices are implemented.