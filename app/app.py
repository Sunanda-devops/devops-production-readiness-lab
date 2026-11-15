import os

from flask import Flask, jsonify


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["APP_VERSION"] = os.getenv("APP_VERSION", "0.1.0")

    @app.get("/")
    def index():
        return jsonify(
            {"service": "production-readiness-api", "version": app.config["APP_VERSION"]}
        )

    @app.get("/health")
    def health():
        return jsonify({"status": "healthy"}), 200

    @app.get("/ready")
    def ready():
        return jsonify({"status": "ready"}), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", "8080")))
