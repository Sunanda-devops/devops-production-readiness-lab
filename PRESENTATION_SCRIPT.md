# DevOps Production-Readiness Lab — Presentation Script

## Slide 1 — Project objective

**On slide:** A production-oriented DevOps reference project for AWS and EKS.

**Speaker notes:**

This project demonstrates how to take a small application from source code to a secure, repeatable delivery workflow. It combines a Flask service, container packaging, Terraform infrastructure, Kubernetes deployment manifests, automated testing, and security gates in GitHub Actions. The goal is not to claim that production infrastructure already exists, but to provide a reviewable foundation that can be adapted to real AWS environments.

## Slide 2 — High-level architecture

**On slide:** Developer → GitHub → GitHub Actions → GHCR → EKS.

**Speaker notes:**

A developer pushes code or opens a pull request. GitHub Actions runs tests and quality checks, scans the repository for secrets and vulnerabilities, builds the container, and scans the image. On a protected main-branch push, the image is published to GitHub Container Registry with an immutable commit-SHA tag. A separate manual deployment path can update an EKS workload after the required production environment approvals.

## Slide 3 — Application and container security

**On slide:** Flask API, health endpoints, multi-stage Dockerfile, non-root runtime.

**Speaker notes:**

The sample service exposes a root endpoint plus `/health` and `/ready` endpoints. These contracts support load-balancer health checks and Kubernetes liveness and readiness probes. The Dockerfile uses a multi-stage build, a slim Python runtime, a non-root user, and a container health check. Compose adds a read-only filesystem, dropped capabilities, and `no-new-privileges`. Configuration comes from environment variables, while real secrets are intentionally excluded from the repository.

## Slide 4 — Terraform AWS foundation

**On slide:** VPC → private subnets → NAT → EKS control plane → managed node group.

**Speaker notes:**

Terraform uses version-pinned community modules to create a VPC with public and private subnets across three availability zones. Worker nodes are placed in private subnets. NAT provides controlled outbound access for private workloads. The EKS module creates the control plane, managed node group, required IAM roles, and cluster networking. The EKS API public endpoint is disabled by default, reducing direct internet exposure. The configuration also enables IRSA, allowing Kubernetes workloads to receive narrowly scoped AWS permissions through OIDC rather than relying on node-wide static credentials.

## Slide 5 — Security groups and remaining AWS hardening

**On slide:** Control-plane SG ↔ node SG; private network boundaries.

**Speaker notes:**

The VPC and EKS modules create and connect the security groups required for cluster and node communication. This is a secure baseline, but it is not the end of the security review. Before production, the generated ingress and egress rules should be inspected and restricted to the required ports and destinations. Production hardening should also add encrypted Terraform remote state with locking, separate AWS accounts or environments, control-plane logging, KMS encryption requirements, restricted egress, and a formal IAM review.

## Slide 6 — Kubernetes runtime security

**On slide:** Deployment, probes, limits, PDB, restricted pod security.

**Speaker notes:**

The Kubernetes manifests create a dedicated namespace with restricted Pod Security labels. The Deployment runs multiple replicas, uses rolling updates, defines CPU and memory requests and limits, and includes liveness and readiness probes. Pods run as non-root with the RuntimeDefault seccomp profile. Privilege escalation is disabled, Linux capabilities are dropped, the root filesystem is read-only, and service-account token automounting is disabled. A PodDisruptionBudget helps preserve availability during voluntary disruptions.

## Slide 7 — CI/CD and security gates

**On slide:** Test → lint → secret scan → vulnerability scan → build → image scan → protected deploy.

**Speaker notes:**

Pull requests and pushes run pytest, Ruff, Bandit, Terraform formatting and validation, Gitleaks, and Trivy filesystem scanning. The container job builds the image with BuildKit and scans the exact image that will be published or deployed. On main, the workflow authenticates to GHCR with the built-in GitHub token and the minimal `packages: write` permission. It publishes an immutable commit-SHA tag instead of relying on the mutable `latest` tag. Deployment is manual, protected by a GitHub environment, and checks rollout status.

## Slide 8 — Production-readiness roadmap

**On slide:** Secrets, identity, observability, policy, resilience.

**Speaker notes:**

The next production steps are explicit. Integrate AWS Secrets Manager or Parameter Store through External Secrets or the Secrets Store CSI Driver. Replace long-lived kubeconfig deployment with GitHub OIDC and short-lived AWS credentials. Add network policies, TLS ingress, WAF or rate limiting, image signing, admission control, centralized logs, metrics, alerts, SLOs, backups, and disaster-recovery testing. Finally, use remote locked Terraform state and require plan review for infrastructure changes.

## Closing

**Speaker notes:**

This lab shows a complete DevOps delivery path with security built into the workflow rather than added after deployment. It provides a practical baseline for an AWS DevOps engineer to extend into a real multi-environment EKS platform while keeping infrastructure changes reviewable, credentials out of source control, and releases traceable to tested commits.
