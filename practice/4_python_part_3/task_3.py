"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>>is_http_domain('http://wikipedia.org')
    True
    >>>is_http_domain('https://ru.wikipedia.org/')
    True
    >>>is_http_domain('griddynamics.com')
    False
"""

import re

# ^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}/?$


def is_http_domain(domain: str) -> bool:
    pattern = r"^https?://([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}/?$"
    return bool(re.fullmatch(pattern, domain))


"""
write tests for is_http_domain function
"""


def test_http_domain_positive():
    assert is_http_domain("http://wikipedia.org") is True


def test_https_domain_positive():
    assert is_http_domain("https://ru.wikipedia.org/") is True


def test_http_domain_negative():
    assert is_http_domain("griddynamics.com") is False


def test_domain_with_hyphen():
    assert is_http_domain("http://my-cool-site.net") is True


def test_domain_with_path_is_invalid():
    assert is_http_domain("http://example.com/some/path") is False


def test_domain_with_invalid_characters():
    assert is_http_domain("https'://my!domain.com/") is False


def test_incomplete_domain():
    assert is_http_domain("https://mydomain") is False
