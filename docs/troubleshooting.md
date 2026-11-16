# Troubleshooting guide

## `ModuleNotFoundError: No module named app`

Run commands from the repository root and install dependencies in the active virtual environment. The project configures pytest with `pythonpath = ["."]`.

```bash
. .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
```

## Port 8080 is already in use

Set a different local port:

```bash
PORT=8090 python -m app.app
```

For Compose, set `PORT=8090` in `.env`; the container still listens internally on port 8080.

## Docker build fails because the daemon is unavailable

Start Docker Engine or Docker Desktop and verify:

```bash
docker info
docker compose version
```

The Python test path does not require Docker.

## Gitleaks or Trivy fails in GitHub Actions

Read the artifact and identify whether the result is a real credential, dependency vulnerability, or infrastructure misconfiguration. Revoke exposed credentials first. Do not silence a finding by adding a broad allowlist. Update dependencies or document a narrowly scoped, reviewed exception.

## Terraform provider or module initialization fails

Check network access and Terraform version. Run:

```bash
terraform version
terraform init -upgrade
terraform validate
```

Do not delete state or run `terraform destroy` as a first troubleshooting step.

## EKS pods remain Pending

Inspect scheduling, capacity, and events:

```bash
kubectl -n production-rollout get pods -o wide
kubectl -n production-rollout describe pod <pod-name>
kubectl get nodes
```

Common causes include unavailable node capacity, invalid image names, insufficient resources, or private-subnet egress problems.

## Deployment fails readiness checks

Check the logs and probe path:

```bash
kubectl -n production-rollout logs deploy/production-readiness-api
kubectl -n production-rollout describe deploy/production-readiness-api
kubectl -n production-rollout port-forward svc/production-readiness-api 8080:80
curl http://localhost:8080/ready
```

The readiness endpoint must return HTTP 200 before the Service receives traffic.
