# Security Review and Hardening Plan

## Current controls

- No credentials or tokens are committed; `.env` and Terraform variable/state files are ignored.
- Gitleaks scans the full repository history in CI.
- Trivy scans the filesystem and built container image for vulnerabilities.
- The container uses a slim base image, a non-root user, a read-only filesystem in Compose, dropped Linux capabilities, and `no-new-privileges`.
- Kubernetes uses a non-root security context, probes, resource limits, and a PodDisruptionBudget.
- The application has separate health and readiness endpoints.

## Required before production

1. Store application secrets in AWS Secrets Manager or Parameter Store and mount them through the External Secrets Operator or a CSI driver. Do not put secrets in ConfigMaps.
2. Replace the sample kubeconfig deployment path with GitHub OIDC and short-lived AWS credentials, then restrict the IAM role trust policy to the repository and protected environment.
3. Pin GitHub Actions to immutable commit SHAs after selecting an approved version and enable Dependabot or Renovate for updates.
4. Add network policies, an ingress controller with TLS, WAF/rate limiting, and centralized audit logs.
5. Enable ECR image signing and admission enforcement with Kyverno or Gatekeeper.
6. Add integration tests against an ephemeral cluster or a staging namespace.
7. Define backup, disaster recovery, SLO, alerting, and incident-response procedures.
8. Run Terraform through a remote backend with state locking, separate AWS accounts/environments, and mandatory plan review.

This file is a living review artifact. Every material security finding should include evidence, severity, owner, remediation, and a regression test.
