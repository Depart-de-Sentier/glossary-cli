"""Fixtures for sentier_glossary"""

import locale

import pytest


@pytest.fixture(scope="session", autouse=True)
def set_locale():
    try:
        locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    except locale.Error:
        pytest.skip("locale not available")
