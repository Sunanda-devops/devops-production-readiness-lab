# Contributing

1. Create a branch for each change.
2. Run `make check` and `docker build --tag production-readiness-api:local .` locally.
3. Never commit credentials, Terraform state, `.env`, kubeconfigs, or production data.
4. Include tests and documentation for behavior or infrastructure changes.
5. Open a pull request and wait for all required CI checks before merging.

Infrastructure changes require a plan review. Production deployment requires an approved protected environment.
