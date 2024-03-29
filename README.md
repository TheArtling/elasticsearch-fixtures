# Elasticsearch Fixtures

This tool is heavily inspired by [klen's Mixer](https://github.com/klen/mixer).

This tool is optimized to be used with `Django` and `pytest`.

It allows you to add documents to a test-index in yout Elasticsearch instance
when you run your unittests.

WARNING: This does not work when you run your tests in parallel. Since it does not create an in-memory ES instance for each test, parallel tests will affect their shared ES instance and that can mess things up.

With `elasticsearch_fixtures` you can do something like this:

```py
from elasticsearch_fixtures.es_mixer import ESMixer

es_mixer = ESMixer(host='http://localhost:9200/')

def test_something():
  doc1 = es_mixer.blend('indexname', id=1, title='test')
  assert doc1['source']['title'] == 'test'
```

Note: If you provide an `id` and a document with that `id` already exists, that
document will not be updated, but fully replaced.

You can also create documents without providing an `id`. Elasticsearch will then
auto-create an `id`:

```py
def test_something():
  doc1 = es_mixer.blend('indexname', title='test')
  print(doc1['id'])
```

And you can update an existing document that is already in the index:

```py
def test_something():
  es_mixer.blend('indexname', id=1, title='test')
  doc1 = es_mixer.update('indexname', id=1, title='new title')
  assert doc1['source']['title'] == 'new_title'
```

Big word of warning: We are no ES experts. We have only started using ES around
June 2019 and one of the first problems that we had was that we did not know how
to properly write unittests for our Django views and Graphene resolver
functions. There are probably much better ways to do this. If you know one, we
would love to hear about it (just open an issue and tell us about it!).

# Installation

```
pip install elasticsearch-fixtures
```

# Configuration

In order to make sure that your tests wipe the index at the very beginning and
also after each test, create the following `conftest.py`:

```py
"""Global settings for pytest."""
import pytest

from django.conf import settings

from elasticsearch_fixtures.es_mixer import ESMixer

es_mixer = ESMixer(host=settings.ELASTICSEARCH_HOST)
index = settings.ELASTICSEARCH_INDEX


@pytest.fixture(scope='session', autouse=True)
def setup_elasticsearch():
    es_mixer.wipe_index(index)


@pytest.fixture(autouse=True)
def cleanup_elasticsearch():
    yield
    es_mixer.wipe_index(index)
```

As you can see, in this example we also use a Django setting called
`ELASTICSEARCH_HOST` (with a trailing slash) and `ELASTICSEARCH_INDEX`. Of
course you can name your own settings however you like.
