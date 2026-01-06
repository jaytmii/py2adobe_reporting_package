"""A test file for all the exceptions"""
from unittest.mock import patch, Mock
import pytest
from py2adobe_reporting.reporting_api import ReportingAPI

def test_status_handling_200():
    """Test that 200 status returns OK message"""
    api = ReportingAPI()
    mock_response = Mock(status_code=200)

    result = api.status_handling(mock_response)
    assert result == "OK"

def test_status_handling_202():
    """Test that 202 status returns Accepted message"""
    api = ReportingAPI()
    mock_response = Mock(status_code=202)

    result = api.status_handling(mock_response)
    assert "Accepted" in result

def test_status_handling_400():
    """Test that 400 status raises MalformedRequest"""
    api = ReportingAPI()
    mock_response = Mock(status_code=400)

    with pytest.raises(ReportingAPI.MalformedRequest) as exc_info:
        api.status_handling(mock_response)
    assert str(exc_info.value) == "Malformed Request"

def test_status_handling_401():
    """Test that 401 status raises UnauthorizedRequest"""
    api = ReportingAPI()
    mock_response = Mock(status_code=401)

    with pytest.raises(ReportingAPI.UnauthorizedRequest) as exc_info:
        api.status_handling(mock_response)
    assert str(exc_info.value) == "Unauthorized Request"

def test_status_handling_403():
    """Test that 403 status raises ForbiddenRequest"""
    api = ReportingAPI()
    mock_response = Mock(status_code=403)

    with pytest.raises(ReportingAPI.ForbiddenRequest) as exc_info:
        api.status_handling(mock_response)
    assert str(exc_info.value) == "Forbidden Request"

def test_status_handling_404():
    """Test that 404 status raises ResourceNotFound"""
    api = ReportingAPI()
    mock_response = Mock(status_code=404)

    with pytest.raises(ReportingAPI.ResourceNotFound) as exc_info:
        api.status_handling(mock_response)
    assert str(exc_info.value) == "Resource Not Found"

def test_status_handling_500():
    """Test that 500 status raises InternalServerError"""
    api = ReportingAPI()
    mock_response = Mock(status_code=500)

    with pytest.raises(ReportingAPI.InternalServerError) as exc_info:
        api.status_handling(mock_response)
    assert str(exc_info.value) == "Internal Server Error"

def test_status_handling_unknown_4xx():
    """Test unknown 4xx error raises ClientError"""
    api = ReportingAPI()
    mock_response = Mock(status_code=418)

    with pytest.raises(ReportingAPI.ClientError) as exc_info:
        api.status_handling(mock_response)
    assert str(exc_info.value) == "CJA Reporting API error"

def test_status_handling_unknown_5xx():
    """Test unknown 5xx error raises InternalServerError"""
    api = ReportingAPI()
    mock_response = Mock(status_code=503)

    with pytest.raises(ReportingAPI.InternalServerError) as exc_info:
        api.status_handling(mock_response)
    assert str(exc_info.value) == "Internal Server Error"

