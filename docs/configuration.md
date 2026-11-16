# Configuration reference

## Application environment variables

| Variable | Default | Purpose |
|---|---|---|
| `APP_VERSION` | `0.1.0` | Version returned by the service metadata endpoint. |
| `ENVIRONMENT` | `local` | Environment label returned by the root endpoint. |
| `PORT` | `8080` | Local application listening port. |
| `LOG_LEVEL` | `INFO` | Python logging level. |

Copy `.env.example` to `.env` for local use. `.env` is ignored by Git. Do not place credentials in this file for shared environments.

## Terraform variables

The example file defines `aws_region`, `project_name`, `environment`, `cluster_version`, `vpc_cidr`, `availability_zones`, and `node_instance_types`. Set environment-specific values in an untracked `terraform.tfvars` file or pass them through a secure CI variable.

Terraform state contains sensitive infrastructure metadata. Use an encrypted remote backend with locking before managing shared or production environments.

## GitHub Actions settings

The normal CI path requires no custom secret. The optional manual deployment path requires:

- Repository variable: `DEPLOY_ENABLED=true`.
- Protected `production` environment.
- Short-lived deployment credentials. The current lab fallback is `KUBE_CONFIG_B64`; prefer AWS OIDC and EKS access entries for production.

## Kubernetes image configuration

Replace the example image in `k8s/deployment.yaml` with an immutable GHCR tag or digest. Do not deploy `latest`.
