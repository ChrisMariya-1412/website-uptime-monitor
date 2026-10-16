from monitor import check_website


def test_google_is_reachable():
    result = check_website("https://www.google.com")

    assert result["status_code"] is not None
    assert result["latency_ms"] is not None
    assert result["latency_ms"] >= 0
    assert result["is_up"] is True