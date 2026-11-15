# DevOps Production Readiness Lab

A production-oriented reference project for an AWS DevOps workflow. It packages a small Flask health service with Docker, Terraform-managed AWS foundations, Kubernetes manifests for EKS, and GitHub Actions quality and security gates.

## What is included

- **Application:** Python 3.12 Flask service with `/`, `/health`, and `/ready` endpoints.
- **Quality:** pytest, Ruff, and Bandit checks.
- **Containerization:** non-root multi-stage Docker image and Compose for local execution.
- **Infrastructure:** Terraform for an EKS cluster, managed node group, VPC, and OIDC provider using the `terraform-aws-modules` modules.
- **Kubernetes:** namespace, ConfigMap, Deployment, Service, PodDisruptionBudget, and optional Ingress with probes and restrictive security context.
- **CI/CD:** GitHub Actions for tests, Gitleaks, Terraform validation, Trivy filesystem and image scanning, and a manually enabled deployment job.

## Quick start

```bash
cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
ruff check .
bandit -r app -ll
python -m app.app
```

The service listens on `http://localhost:8080` by default.

### Docker

```bash
docker compose up --build
curl http://localhost:8080/health
```

The image runs as an unprivileged user and accepts configuration through environment variables. Never commit `.env` files or real credentials.

## AWS and EKS deployment

1. Configure AWS credentials outside the repository using a secure mechanism such as GitHub OIDC, an AWS profile, or a workload identity provider.
2. Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` and set values for your account and region. The `.gitignore` excludes `*.tfvars` except the example file.
3. Review the plan carefully, then run:

```bash
cd terraform
terraform init
terraform fmt -check
terraform validate
terraform plan -out=tfplan
terraform apply tfplan
```

4. Configure `kubectl` from the Terraform outputs, update the image reference in `k8s/deployment.yaml`, and apply the manifests:

```bash
aws eks update-kubeconfig --region "$AWS_REGION" --name "$EKS_CLUSTER_NAME"
kubectl apply -f k8s/
kubectl -n production-rollout rollout status deployment/production-readiness-api
```

The Terraform module creates paid AWS resources. Review cost, network, IAM, encryption, and retention requirements before applying in a real account. Destroying the stack is also a deliberate action: `terraform destroy`.

## GitHub Actions setup

Every push and pull request runs tests, linting, Bandit, Terraform formatting/validation, Gitleaks, and Trivy filesystem scanning. A container is built and scanned with Trivy before any deployment.

For the optional manual deployment path, configure these repository settings only after reviewing the workflow:

- Repository variable `DEPLOY_ENABLED=true`.
- Repository or environment secret `KUBE_CONFIG_B64` containing a base64-encoded, short-lived kubeconfig.
- A protected GitHub environment named `production` with required reviewers.

The workflow does not contain cloud credentials or a cluster endpoint. Prefer GitHub OIDC and short-lived AWS credentials for a production implementation.

## Repository conventions

- Keep secrets in a secret manager or CI secret store; use `.env.example` only for names and safe examples.
- Pin or regularly review third-party GitHub Actions and container base image versions.
- Add an issue and pull request review for infrastructure changes.
- Run `make check` before opening a pull request.

See [`SECURITY_REVIEW.md`](SECURITY_REVIEW.md) for the threat model and planned hardening work.
