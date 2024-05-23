import pytest
from requests.exceptions import RequestException

from sentier_glossary import CommonSchemes, GlossaryAPI


def test_concept():
    api = GlossaryAPI(language_code="fr")
    expected = {
        "iri": "http://data.europa.eu/xsp/cn2024/580710000080",
        "notation": "5807 10",
        "prefLabel": "5807 10 - tissés",
        "identifier": "580710000080",
        "scopeNote": "Étiquettes, écussons et articles simil. en matières textiles, en pièces, en rubans ou découpés, tissés, non brodés",
        "altLabels": ["- tissés"],
        "concept_schemes": ["http://data.europa.eu/xsp/cn2024/cn2024"],
        "relations": [
            {
                "type": "broader",
                "source_concept_iri": "http://data.europa.eu/xsp/cn2024/580710000080",
                "target_concept_iri": "http://data.europa.eu/xsp/cn2024/580700000080",
            },
            {
                "type": "broader",
                "source_concept_iri": "http://data.europa.eu/xsp/cn2024/580710100080",
                "target_concept_iri": "http://data.europa.eu/xsp/cn2024/580710000080",
            },
            {
                "type": "broader",
                "source_concept_iri": "http://data.europa.eu/xsp/cn2024/580710900080",
                "target_concept_iri": "http://data.europa.eu/xsp/cn2024/580710000080",
            },
        ],
    }
    assert api.concept("http://data.europa.eu/xsp/cn2024/580710000080") == expected


def test_concept_missing():
    api = GlossaryAPI()
    with pytest.raises(RequestException):
        api.concept("http://data.europa.jupiter")
