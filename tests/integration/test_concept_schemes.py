from sentier_glossary import GlossaryAPI


def test_concept_schemes_plain():
    api = GlossaryAPI()
    expected = {
        "iri": "http://data.europa.eu/z1e/icstcom2009/icst",
        "notation": "ICST-COM 2009",
        "prefLabel": "International Classification of Ship by Type (ICST-COM)",
        "scopeNote": "",
    }
    assert expected in api.schemes()


def test_concept_schemes_change_language():
    api = GlossaryAPI()
    api.set_language_code("fr")
    expected = {
        "iri": "http://data.europa.eu/z1e/icstcom2009/icst",
        "notation": "ICST-COM 2009",
        "prefLabel": "Classification internationale des types de navires (ICST-COM)",
        "scopeNote": "",
    }
    assert expected in api.schemes()
