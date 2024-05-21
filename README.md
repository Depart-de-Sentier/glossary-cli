# sentier_glossary

[![PyPI](https://img.shields.io/pypi/v/sentier_glossary.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/sentier_glossary.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/sentier_glossary)][pypi status]
[![License](https://img.shields.io/pypi/l/sentier_glossary)][license]

[![Read the documentation at https://sentier_glossary.readthedocs.io/](https://img.shields.io/readthedocs/sentier_glossary/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/Depart-de-Sentier/sentier_glossary/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/Depart-de-Sentier/sentier_glossary/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/sentier_glossary/
[read the docs]: https://sentier_glossary.readthedocs.io/
[tests]: https://github.com/Depart-de-Sentier/sentier_glossary/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/Depart-de-Sentier/sentier_glossary
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _sentier_glossary_ via [pip] from [PyPI]:

```console
$ pip install sentier_glossary
```

## Usage

There is a single class, `GlossaryAPI`, which wraps the [Sentier glossary API endpoints](https://api.g.sentier.dev/latest/docs#/):

```python
from sentier_glossary import GlossaryAPI, CommonSchemes
api = GlossaryAPI()
```

With this class, you can retrieve the collections (logical organization of concept schemes into products, processes, places, and units), [concept schemes](https://www.w3.org/TR/2005/WD-swbp-skos-core-guide-20051102/#secscheme), and [concepts](https://www.w3.org/TR/2005/WD-swbp-skos-core-guide-20051102/#secconcept). For example:

```python
> api.schemes()
[{'iri': 'http://data.europa.eu/z1e/icstcom2009/icst',
  'notation': 'ICST-COM 2009',
  'prefLabel': 'International Classification of Ship by Type (ICST-COM)',
  'scopeNote': ''},
...]
> [
>    concept
>    for concept in api.concepts_for_scheme('http://data.europa.eu/z1e/icstcom2009/icst')
>    if 'passenger' in concept['prefLabel'].lower()
> ]
[{'iri': 'http://data.europa.eu/z1e/icstcom2009/35',
  'identifier': '35',
  'notation': '35',
  'prefLabel': '35 Passenger ship',
  'altLabel': 'Passenger ship',
  'scopeNote': 'Ship categories included: passengers (excluding cruise passengers). This category should be subdivided into: a) High speed passenger ship specialised meeting the requirements set out in the IMO HSC Code paragraph 1.4.30; b) Other passenger ships. A ship designed with one or more decks specifically for the carriage of passengers, and where there is either no cabin accommodation for the passengers (un- berthed) or not all of the passengers are accommodated in cabins where cabins are provided, is sometimes referred to as a “ferry”. Ro-Ro passenger ships are excluded.'},
 {'iri': 'http://data.europa.eu/z1e/icstcom2009/36',
  'identifier': '36',
  'notation': '36',
  'prefLabel': '36 Cruise Passenger',
  'altLabel': 'Cruise Passenger',
  'scopeNote': 'Ship categories included: cruise ships only '}]
> api.concept('http://data.europa.eu/z1e/icstcom2009/35')
{'iri': 'http://data.europa.eu/z1e/icstcom2009/35',
 'notation': '35',
 'prefLabel': '35 Passenger ship',
 'identifier': '35',
 'scopeNote': 'Ship categories included: passengers (excluding cruise passengers). This category should be subdivided into: a) High speed passenger ship specialised meeting the requirements set out in the IMO HSC Code paragraph 1.4.30; b) Other passenger ships. A ship designed with one or more decks specifically for the carriage of passengers, and where there is either no cabin accommodation for the passengers (un- berthed) or not all of the passengers are accommodated in cabins where cabins are provided, is sometimes referred to as a “ferry”. Ro-Ro passenger ships are excluded.',
 'altLabel': 'Passenger ship',
 'concept_schemes': ['http://data.europa.eu/z1e/icstcom2009/icst'],
 'relations': []}
```

The Sentier glossary uses vocabularies built on [SKOS](https://www.w3.org/TR/2005/WD-swbp-skos-core-guide-20051102/), and uses SKOS terms like `prefLabel`, `altLabel`, `broader`, `narrower`, and `scopeNote`.

### Language of Results

The results returned from the API will depend on your language preferences. For example:



By default, the glossary client uses your default [language in your locale](https://en.wikipedia.org/wiki/Locale_(computer_software)). You can change it when instantiating the API:

```python
api = GlossaryAPI(language_code="fr")
```

You can also use `set_language_code()` to change the language of an existing `GlossaryAPI` client.


## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License

Distributed under the terms of the [MIT license][License],
_sentier_glossary_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


<!-- github-only -->

[command-line reference]: https://sentier_glossary.readthedocs.io/en/latest/usage.html
[License]: https://github.com/Depart-de-Sentier/sentier_glossary/blob/main/LICENSE
[Contributor Guide]: https://github.com/Depart-de-Sentier/sentier_glossary/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/Depart-de-Sentier/sentier_glossary/issues
