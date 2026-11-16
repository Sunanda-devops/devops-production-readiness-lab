# Operations, observability, and recovery

## Observability

The service exposes Prometheus text-format metrics at `/metrics` and writes request completion logs containing method, path, status, duration, and request ID. Use the example `monitoring/servicemonitor.yaml.example` with the Prometheus Operator and build Grafana panels for request rate, error rate, latency, pod restarts, CPU, and memory.

For a production platform, forward structured logs to CloudWatch, Loki, or an equivalent managed logging system. Add alerts for failed readiness probes, elevated 5xx responses, high latency, node pressure, and deployment rollout failures.

## Backup and recovery pattern

This sample API is stateless and has no database to back up. For stateful services, use managed database snapshots and an AWS S3 bucket with versioning, encryption, lifecycle retention, and restricted IAM access. Test restores on a schedule and record recovery point and recovery time objectives.

Do not put backup credentials in manifests or pipelines. Use workload identity, short-lived credentials, and a separate recovery procedure. A production runbook should cover restore validation, DNS or ingress recovery, secret rotation, and rollback.
