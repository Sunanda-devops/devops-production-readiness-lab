# Resume-to-repository alignment

This project was checked against the latest resume. No resume PDF or personal contact data is stored in this repository.

## Evidence represented in this repository

- **Python and Flask:** `app/app.py` implements a working service with health, readiness, metrics, request IDs, and structured errors.
- **Docker and Docker Compose:** the multi-stage `Dockerfile` and hardened Compose profile run the service as a non-root user.
- **AWS, Terraform, EKS, and Kubernetes:** `terraform/` and `k8s/` provide a reviewable VPC/EKS foundation and restricted workload manifests.
- **GitHub Actions, Gitleaks, Bandit, and Trivy:** `.github/workflows/ci-cd.yml` implements automated quality, secret, filesystem, and container checks.
- **Helm:** `helm/production-readiness-api/` packages the same workload with configurable values and security defaults.
- **Jenkins:** `Jenkinsfile` provides a parallel CI path for teams using Jenkins.
- **Prometheus/Grafana:** `/metrics` exposes Prometheus text format and `monitoring/` contains a ServiceMonitor example and dashboard guidance.
- **Technical writing and troubleshooting:** `README.md`, `docs/installation.md`, `docs/configuration.md`, `docs/troubleshooting.md`, and `SECURITY_REVIEW.md` document setup and operational decisions.

## Resume claims intentionally not represented as completed implementation here

- Azure AKS, AWS CodeBuild, Bitbucket, Ansible, Loki, Fluent Bit, S3 backup/restore, ArgoCD, EFS, ALB, FastAPI, PostgreSQL, MySQL, React, and TypeScript belong to other projects or professional experience. They should not be presented as implemented by this repository.
- Real AWS resources have not been provisioned by this repository commit. Terraform is an apply-ready template that still requires account-specific review, state configuration, credentials, and explicit approval.
- The deployment workflow contains a documented lab fallback for kubeconfig. Production should use GitHub OIDC and EKS access entries with short-lived credentials.

## Recommended portfolio links

Use the project links from the resume for the broader portfolio. Use this repository specifically to demonstrate production-readiness controls, container security, Terraform/EKS design, Kubernetes hardening, CI quality gates, and operational documentation.
