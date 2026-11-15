from app.app import create_app


def test_root_returns_service_metadata():
    client = create_app().test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["service"] == "production-readiness-api"


def test_health_endpoint():
    response = create_app().test_client().get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_readiness_endpoint():
    response = create_app().test_client().get("/ready")
    assert response.status_code == 200
    assert response.json == {"status": "ready"}
