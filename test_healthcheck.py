from unittest.mock import patch
from healthcheck import check_endpoint
from urllib.error import HTTPError
from urllib.error import HTTPError, URLError

def test_200_response_is_healthy():
    with patch("healthcheck.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.status = 200

        result = check_endpoint("https://example.com")

    assert result["healthy"] is True
    assert result["status_code"] == 200
    assert result["error"] is None
    

def test_204_response_is_healthy():
    with patch("healthcheck.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.status = 204

        result = check_endpoint("https://example.com")

    assert result["healthy"] is True
    assert result["status_code"] == 204
    assert result["error"] is None

def test_404_response_is_healthy():
    url = "https://example.com/missing"

    with patch("healthcheck.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = HTTPError(url, 404, "Not Found",None, None)

        result = check_endpoint(url)

    assert result["healthy"] is False
    assert result["status_code"] == 404
    assert "Not Found" in result["error"]

def test_connection_failure_is_unhealthy():
    url = "https://example.com"

    with patch("healthcheck.urlopen") as mock_urlopen:
        mock_urlopen.side_effect = URLError("Connection refused")

        result = check_endpoint(url)

    assert result["healthy"] is False
    assert result["status_code"] is None
    assert "Connection refused" in result["error"]

