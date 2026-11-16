# Installation and local development

## Prerequisites

Install Python 3.12+, Docker Engine with Compose v2, Git, and optionally Terraform, AWS CLI, kubectl, and Helm for the AWS path.

## Run locally with Python

```bash
git clone https://github.com/Sunanda-devops/devops-production-readiness-lab.git
cd devops-production-readiness-lab
cp .env.example .env
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
make check
python -m app.app
```

Open `http://localhost:8080/` and verify:

```bash
curl -i http://localhost:8080/health
curl -i http://localhost:8080/ready
curl http://localhost:8080/metrics
```

## Run with Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

The Compose service maps port `8080`, runs as a non-root user, uses a read-only filesystem, and drops Linux capabilities. Stop it with `docker compose down`.

## Validate Terraform without provisioning

```bash
cd terraform
terraform init -backend=false
terraform fmt -check -recursive
terraform validate
terraform plan -var-file=terraform.tfvars.example
```

The plan command is safe to review but AWS resource creation starts only with `terraform apply`. The module creates paid resources; use a dedicated account or environment and review the plan carefully.

## Deploy to EKS

1. Configure AWS credentials through a profile or short-lived OIDC credentials.
2. Copy `terraform.tfvars.example` to `terraform.tfvars` and set your region and environment.
3. Run `terraform init`, `terraform plan -out=tfplan`, review, and apply the approved plan.
4. Configure kubectl using the cluster name and region outputs.
5. Push an image to GHCR or update the image reference in `k8s/deployment.yaml`.
6. Apply `k8s/namespace.yaml` and `k8s/deployment.yaml`.
7. Verify rollout and service health.

Never commit Terraform state, plans, kubeconfig files, or production credentials.
