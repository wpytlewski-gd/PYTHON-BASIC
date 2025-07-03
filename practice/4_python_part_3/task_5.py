"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""

from typing import Tuple
from unittest.mock import Mock, patch
from urllib import request
from urllib.parse import urlparse

import pytest


def make_request(url: str) -> Tuple[int, str]:
    parsed_url = urlparse(url)
    if parsed_url.scheme not in ("http", "https"):
        raise ValueError(f"Invalid URL scheme '{parsed_url.scheme}'. Only 'http' and 'https' are allowed.")

    with request.urlopen(url) as response:
        data = response.read().decode("utf-8")
        return response.status, data


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""


@patch("urllib.request.urlopen")
def test_make_request_success(mock_urlopen):
    mock_response = Mock()
    mock_response.status = 200
    mock_response.read.return_value = b"Mocked response data"
    mock_urlopen.return_value.__enter__.return_value = mock_response

    status, data = make_request("https://example.com")
    assert status == 200
    assert data == "Mocked response data"
    mock_urlopen.assert_called_once_with("https://example.com")


@patch("urllib.request.urlopen")
def test_make_request_invalid_scheme(mock_urlopen):
    with pytest.raises(ValueError, match="Invalid URL scheme 'ftp'"):
        make_request("ftp://example.com")
    mock_urlopen.assert_not_called()


@patch("urllib.request.urlopen")
def test_make_request_no_scheme(mock_urlopen):
    with pytest.raises(ValueError, match="Invalid URL scheme ''"):
        make_request("example.com")
    mock_urlopen.assert_not_called()
