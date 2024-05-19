import locale
from unittest.mock import Mock, patch, call, ANY
import sentier_glossary as g

@patch("requests.get")
def test_search_returns_concepts(mock: Mock):
    api = g.GlossaryAPI()
    search = api.search("coconut")
    assert mock.called

@patch("requests.get")
@patch("locale.getlocale")
def test_lang(loc: Mock, r: Mock):
    loc.return_value = ("pt_PT", "UTF-8")
    api = g.GlossaryAPI()
    assert api.get_language_code() == "pt"
    schemes = api.schemes()
    r.assert_has_calls([
        call(ANY, params={"lang": "pt"})
        ])
