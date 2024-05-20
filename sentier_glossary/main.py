import itertools
import locale
import warnings
from collections import defaultdict
from enum import Enum
from urllib.parse import urljoin, urlparse

import requests
import torch
from sentence_transformers import SentenceTransformer, util  # type: ignore

from sentier_glossary.settings import Settings


class CommonSchemes(Enum):
    cn2024 = "http://data.europa.eu/xsp/cn2024/cn2024"
    nace21 = "http://data.europa.eu/ux2/nace2.1/nace2.1"
    low2015 = "http://data.europa.eu/6p8/low2015/scheme"
    icst2009 = "http://data.europa.eu/z1e/icstcom2009/icst"
    prodcom2023 = "http://data.europa.eu/qw1/prodcom2023/prodcom2023"
    isic4 = "https://unstats.un.org/classifications/ISIC/rev4/scheme"


DEFAULT_COMPONENTS = {
    "process": CommonSchemes.cn2024,
    "product": CommonSchemes.nace21,
    "unit": None,
    "place": None,
}

cfg = Settings()


class GlossaryAPI:
    def __init__(self, base_url: str = cfg.base_url, default_language: str | None = None):
        self.base_url = base_url
        if not self.base_url.endswith("/"):
            self.base_url += "/"

        self._semantic_search = False
        self.language_code = self.get_language_code()
        print(f"Using language code '{self.language_code}'; change with `set_language_code()`")

    @property
    def _params(self) -> dict:
        """Default parameters for every request."""
        return {"lang": self.language_code}

    def get_language_code(self, default: str = "en") -> str:
        """Get 2-letter (Set 1) ISO 639 language code."""
        code = locale.getlocale()[0] or default
        if isinstance(code, str) and len(code) >= 2:
            return code[:2]
        raise ValueError(f"Invalid language code {code} found; set locale or `default_language`")

    def set_language_code(self, language_code: str) -> None:
        """Override language code from system locale or input argument."""
        if not isinstance(language_code, str) and len(language_code) >= 2:
            raise ValueError(
                f"Invalid language code {language_code} given. Must be `str` of length two."
            )
        self.language_code = language_code[:2]
        if self._semantic_search:
            warnings.warn(
                f"""Semantic search cache is stale and disabled. Please reenable with
                `setup_semantic_search()` to use semantic search with {self.language_code}."""
            )
            self._semantic_search = False

    def setup_semantic_search(
        self,
        model_id: str = "all-mpnet-base-v2",
        components: dict[str, CommonSchemes | None] = DEFAULT_COMPONENTS,
    ) -> None:
        """Download data and metadata to perform semantic search queries"""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=FutureWarning)
            self._embedder = SentenceTransformer("all-MiniLM-L6-v2")

        self._catalogues: dict[str, str] = {}
        self._semantic_search = True

        for cs in CommonSchemes:
            self._catalogues[cs.value] = defaultdict(list)
            for concept in self.concepts_for_scheme(cs):
                for label in ("prefLabel", "altLabel", "scopeNote"):
                    if concept.get(label):
                        self._catalogues[cs.value][concept[label]].append(concept)

    def schemes(self) -> list[dict]:
        """Get all concept schemes, regardless of type"""
        return requests.get(urljoin(self.base_url, "schemes"), params=self._params).json()[
            "concept_schemes"
        ]

    def _validate_iri(self, iri: str) -> None:
        """Basic IRI validation.

        Args:
            iri (str): The [IRI](https://en.wikipedia.org/wiki/Internationalized_Resource_Identifier)

        Raises:
            ValueError: The IRI is not valid
            KeyError: The requested resource was not found

        """
        pass

    def concepts_for_scheme(self, scheme_iri: str | Enum) -> list[dict]:
        if isinstance(scheme_iri, Enum):
            scheme_iri = scheme_iri.value
        self._validate_iri(scheme_iri)
        data = requests.get(
            urljoin(self.base_url, "concepts"),
            params=self._params | {"concept_scheme_iri": scheme_iri},
        ).json()["concepts"]
        if not data and scheme_iri not in {obj["iri"] for obj in self.schemes()}:
            raise KeyError(f"Given concept scheme IRI '{scheme_iri}' not present in glossary")
        return data

    def concept(self, concept_iri: str) -> dict:
        """Return a single concept resource.

        Args:
            query (str): the search query string
            scope (str, CommonSchemes, None): If given, limit the search to one concept scheme

        Returns:
            A dictionary of the requested resource

        Raises:
            ValueError: The IRI is not valid
            KeyError: The requested resource was not found

        """
        self._validate_iri(concept_iri)
        data = requests.get(
            urljoin(self.base_url, "concepts"),
            params=self._params | {"concept_iri": concept_iri},
        ).json()
        if not data:
            raise KeyError(f"Given concept scheme IRI '{scheme_iri}' not present in glossary")
        return data

    def search(self, query: str) -> list[dict]:
        """Search the the concept library using the `/search` endpoint.

        Args:
            query (str): the search query string
            scope (str, CommonSchemes, None): If given, limit the search to one concept scheme

        Returns:
            list of resources matching the search query.
        """

        return requests.get(
            urljoin(self.base_url, "search"), params=self._params | {"search_term": query}
        ).json()["concepts"]

    def semantic_search(
        self, query: str, scope: str | CommonSchemes | None = None, min_num_results: int = 10
    ) -> list[dict]:
        """Perform semantic search query.

        Stolen shamelessly from https://www.sbert.net/examples/applications/semantic-search/README.html#semantic-search.

        Args:
            query (str): the search query string
            scope (str, CommonSchemes, None): If given, limit the search to one concept scheme
            min_num_results (int): Minimum number of results to return.

        Returns:
            list of results

        """
        if not self._semantic_search:
            self.setup_semantic_search()
        if isinstance(scope, CommonSchemes):
            scope = scope.value
        if scope not in self._catalogues:
            raise KeyError(f"Given scope {scope} not present in semantic search cache.")
        corpus = self._catalogues[scope]
        num_results = min(min_num_results, len(corpus))
        corpus_embeddings = self._embedder.encode(corpus, convert_to_tensor=True)
        query_embedding = self._embedder.encode(query, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        return list(
            itertools.chain(
                self._catalogues[scope][corpus[idx]]
                for _, idx in torch.topk(cos_scores, k=num_results)
            )
        )
