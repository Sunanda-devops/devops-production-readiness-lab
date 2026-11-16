import os
import time
import uuid
from dataclasses import dataclass

from flask import Flask, g, jsonify, request


@dataclass(frozen=True)
class Settings:
    app_version: str
    environment: str
    port: int

    @classmethod
    def from_environment(cls) -> "Settings":
        return cls(
            app_version=os.getenv("APP_VERSION", "0.1.0"),
            environment=os.getenv("ENVIRONMENT", "local"),
            port=int(os.getenv("PORT", "8080")),
        )


def create_app(settings: Settings | None = None) -> Flask:
    settings = settings or Settings.from_environment()
    app = Flask(__name__)
    app.config["SETTINGS"] = settings
    app.config["METRICS"] = {"requests_total": 0, "requests_by_path": {}}
    app.logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    @app.before_request
    def start_request() -> None:
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g.started_at = time.perf_counter()
        metrics = app.config["METRICS"]
        metrics["requests_total"] += 1
        path_counts = metrics["requests_by_path"]
        path_counts[request.path] = path_counts.get(request.path, 0) + 1

    @app.after_request
    def finish_request(response):
        response.headers["X-Request-ID"] = g.request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        elapsed_ms = (time.perf_counter() - g.started_at) * 1000
        app.logger.info(
            "request_complete method=%s path=%s status=%s duration_ms=%.2f request_id=%s",
            request.method,
            request.path,
            response.status_code,
            elapsed_ms,
            g.request_id,
        )
        return response

    @app.get("/")
    def index():
        return jsonify(
            {
                "service": "production-readiness-api",
                "version": settings.app_version,
                "environment": settings.environment,
                "links": {"health": "/health", "ready": "/ready", "metrics": "/metrics"},
            }
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "healthy", "service": "production-readiness-api"}), 200

    @app.get("/ready")
    def ready():
        return jsonify({"status": "ready", "checks": {"application": "ok"}}), 200

    @app.get("/metrics")
    def metrics():
        current = app.config["METRICS"]
        lines = [
            "# HELP app_requests_total Total HTTP requests handled by the application.",
            "# TYPE app_requests_total counter",
            f'app_requests_total {current["requests_total"]}',
        ]
        for path, count in sorted(current["requests_by_path"].items()):
            safe_path = path.replace('\\', '\\\\').replace('"', '\\"')
            lines.append(f'app_requests_by_path_total{{path="{safe_path}"}} {count}')
        return "\n".join(lines) + "\n", 200, {"Content-Type": "text/plain; version=0.0.4"}

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "not_found", "request_id": g.request_id}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "internal_server_error", "request_id": g.request_id}), 500

    return app


app = create_app()


if __name__ == "__main__":
    settings = app.config["SETTINGS"]
    app.run(port=settings.port)
