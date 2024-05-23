import locale
from unittest.mock import ANY, Mock, call, patch

import pytest

import sentier_glossary as g


@patch("requests.get")
@patch("locale.getlocale")
def test_lang(loc: Mock, r: Mock):
    loc.return_value = ("pt_PT", "UTF-8")
    api = g.GlossaryAPI()
    assert api.language_code == "pt"
    api.schemes()
    r.assert_has_calls([call(ANY, params={"lang": "pt"}, timeout=10)])


@patch("locale.getlocale")
def test_lang_manual_setting(loc: Mock):
    loc.return_value = ("pt_PT", "UTF-8")
    api = g.GlossaryAPI(language_code="es")
    assert api.language_code == "es"


def test_locale_lang_blank_string():
    locale.setlocale(locale.LC_ALL, "")
    api = g.GlossaryAPI()
    assert api.language_code == "en"


@patch("locale.getlocale")
def test_locale_invalid(loc: Mock):
    loc.return_value = ("p", "UTF-8")
    with pytest.raises(ValueError):
        g.GlossaryAPI()


@patch("locale.getlocale")
def test_locale_lowercased(loc: Mock):
    loc.return_value = ("PT", "UTF-8")
    api = g.GlossaryAPI()
    assert api.language_code == "pt"


def test_set_language_code():
    api = g.GlossaryAPI()
    api.set_language_code("fr")
    assert api.language_code == "fr"


def test_set_language_code_lowercased():
    api = g.GlossaryAPI()
    api.set_language_code("FR")
    assert api.language_code == "fr"


def test_set_language_code_invalid():
    api = g.GlossaryAPI()
    with pytest.raises(ValueError):
        api.set_language_code("f")

    with pytest.raises(ValueError):
        api.set_language_code(1)
