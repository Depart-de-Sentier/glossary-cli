import pytest

from sentier_glossary import GlossaryAPI


def test_search():
    api = GlossaryAPI()
    expected = {
        "iri": "http://data.europa.eu/ux2/nace2.1/0312",
        "notation": "03.12",
        "prefLabel": "03.12 Freshwater fishing",
        "identifier": "0312",
        "scopeNote": "",
        "altLabels": ["Freshwater fishing"],
    }
    assert expected in api.search("fishing")
