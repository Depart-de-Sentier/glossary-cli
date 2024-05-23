import pandas as pd
import pytest

from sentier_glossary import CommonSchemes, GlossaryAPI


@pytest.fixture()
def api():
    api = GlossaryAPI()
    api.setup_semantic_search(model_id="paraphrase-MiniLM-L3-v2")
    return api


@pytest.mark.slow
def test_semantic_search(api):
    results = api.semantic_search("corn", CommonSchemes.cn2024)
    assert isinstance(results, list)
    for obj in results:
        assert isinstance(obj, dict)
    assert "http://data.europa.eu/xsp/cn2024/100500000080" in {obj["iri"] for obj in results}

    expected = {
        "iri": "http://data.europa.eu/xsp/cn2024/100021000090",
        "prefLabel": "CHAPTER 10 - CEREALS",
    }
    assert any(expected in obj.get("broader") for obj in results)

    # Make sure results are unique
    assert len({obj["iri"] for obj in results}) == len(results)

    # Check min_num_results_param
    results = api.semantic_search("corn", CommonSchemes.cn2024, min_num_results=100)
    assert len(results) >= 30

    # Check dataframe return type
    df = api.semantic_search("corn", CommonSchemes.cn2024, dataframe=True)
    assert isinstance(df, pd.DataFrame)
    assert len(df)
    assert all(
        df.columns == ["prefLabel", "completeLabel", "broader_iri", "broader_prefLabel", "iri"]
    )
