import pytest
from requests.exceptions import RequestException

from sentier_glossary import CommonSchemes, GlossaryAPI


def test_concepts_for_schemes():
    api = GlossaryAPI(language_code="fr")
    expected = {
        "iri": "http://data.europa.eu/z1e/icstcom2009/41",
        "notation": "41",
        "prefLabel": "41 Pêche",
        "identifier": "41",
        "scopeNote": "Catégories incluses dans chaque type de navire: Bateau de pêche, Navire-usine pour le traitement du poisson",
        "altLabels": ["Pêche"],
    }
    assert expected in api.concepts_for_scheme("http://data.europa.eu/z1e/icstcom2009/icst")


def test_concepts_for_schemes_dataclass():
    api = GlossaryAPI(language_code="fr")
    expected = {
        "iri": "http://data.europa.eu/z1e/icstcom2009/41",
        "notation": "41",
        "prefLabel": "41 Pêche",
        "identifier": "41",
        "scopeNote": "Catégories incluses dans chaque type de navire: Bateau de pêche, Navire-usine pour le traitement du poisson",
        "altLabels": ["Pêche"],
    }
    assert expected in api.concepts_for_scheme(CommonSchemes.icst2009)


def test_concepts_for_schemes_missing():
    api = GlossaryAPI()
    with pytest.raises(RequestException):
        api.concepts_for_scheme("http://data.europa.jupiter")
