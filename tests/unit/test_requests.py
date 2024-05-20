from unittest.mock import Mock, patch

import pytest
import requests

import sentier_glossary as g


@patch("requests.get")
def test_requests(mock: Mock):
    api = g.GlossaryAPI()
    s = api.concepts_for_scheme("isic4")
    assert mock.called


@patch("requests.get")
def test_requests_exception(r: Mock):
    r.return_value.raise_for_status.side_effect = requests.exceptions.RequestException()
    r.return_value.status_code = 500

    api = g.GlossaryAPI()
    with pytest.raises(requests.exceptions.RequestException) as e:
        api.search("coconut")

    assert "Error fetching data" in str(e.value)
    assert "HTTP 500" in str(e.value)
