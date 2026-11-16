from app.app import Settings, create_app


def client():
    return create_app(Settings(app_version="test", environment="test", port=8080)).test_client()


def test_root_returns_service_metadata():
    response = client().get("/")
    assert response.status_code == 200
    assert response.json["service"] == "production-readiness-api"
    assert response.json["environment"] == "test"


def test_health_endpoint():
    response = client().get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.headers["X-Request-ID"]


def test_readiness_endpoint():
    response = client().get("/ready")
    assert response.status_code == 200
    assert response.json == {"status": "ready", "checks": {"application": "ok"}}


def test_metrics_endpoint_counts_requests():
    test_client = client()
    test_client.get("/health")
    response = test_client.get("/metrics")
    assert response.status_code == 200
    assert "app_requests_total 2" in response.text
    assert 'app_requests_by_path_total{path="/health"} 1' in response.text


def test_missing_route_returns_traceable_json_error():
    response = client().get("/does-not-exist")
    assert response.status_code == 404
    assert response.json["error"] == "not_found"
    assert response.json["request_id"] == response.headers["X-Request-ID"]
