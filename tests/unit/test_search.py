from unittest.mock import ANY, Mock, call, patch

import sentier_glossary as g


@patch("requests.get")
@patch("locale.getlocale")
def test_lang(loc: Mock, r: Mock):
    loc.return_value = ("pt_PT", "UTF-8")
    api = g.GlossaryAPI()
    assert api.get_language_code() == "pt"
    schemes = api.schemes()
    r.assert_has_calls([call(ANY, params={"lang": "pt"})])
