from unittest.mock import Mock, patch

import sentier_glossary as g


@patch("sentier_glossary.GlossaryAPI._requests_get")
def test_response_schema(r: Mock):
    r.return_value = [
        {
            "iri": "http://data.europa.eu/xsp/cn2024/570220000080",
            "notation": "5702 20 00",
            "prefLabel": "5702 20 00 - Floor coverings of coconut fibres (coir)",
            "identifier": "570220000080",
            "scopeNote": 'Floor coverings of coconut fibres "coir", woven, whether or not made up',
            "altLabel": "- Floor coverings of coconut fibres (coir)",
        },
        {
            "iri": "http://data.europa.eu/xsp/cn2024/200900000080",
            "notation": "2009",
            "prefLabel": "2009 Fruit or nut juices (including grape must and coconut water) and vegetable juices, unfermented and not containing added spirit, whether or not containing added sugar or other sweetening matter",
            "identifier": "200900000080",
            "scopeNote": "Fruit juices, incl. grape must, and vegetable juices, unfermented, not containing added spirit, whether or not containing added sugar or other sweetening matter",
            "altLabel": "Fruit or nut juices (including grape must and coconut water) and vegetable juices, unfermented and not containing added spirit, whether or not containing added sugar or other sweetening matter",
        },
    ]
    labels = [label for label in r.return_value[0].keys()]
    api = g.GlossaryAPI()
    result = api.search("coconut")
    assert len(result) == 2
    assert all(label in result[0] for label in labels)
