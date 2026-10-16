
from monitor import check_website


def test_website_returns_success(monkeypatch):
    class FakeResponse:
        status_code = 200

    def fake_get(url, timeout):
        assert url == "https://example.com"
        assert timeout == 10
        return FakeResponse()

    monkeypatch.setattr("monitor.requests.get", fake_get)

    result = check_website("https://example.com")

    assert result["status_code"] == 200
    assert result["is_up"] is True
    assert result["latency_ms"] >= 0
    assert result["error"] is None


def test_website_connection_failure(monkeypatch):
    import requests

    def fake_get(url, timeout):
        raise requests.ConnectionError("Connection failed")

    monkeypatch.setattr("monitor.requests.get", fake_get)

    result = check_website("https://example.com")

    assert result["is_up"] is False
    assert result["error"] == "Connection failed"
