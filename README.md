# Elasticsearch Fixtures

This tool is heavily inspired by [klen's Mixer](https://github.com/klen/mixer).

It allows you to write unittests for your application and write documents
into your Elasticsearch (ES) instance.

With `elasticsearch_fixtures` you can do something like this:

```py
import pytest

from django.test import RequestFactory

# fictional graphene schema, let's assume this schema has a resolver that
# queries ES and returns an array of found documents
from .. import schema

from elasticsearch_fixtures import es_mixer

class TestMyView:
  def test_my_function(self):
    # let's assume there is a document type `product`
    product1 = es_mixer.blend('product', id=1, title="Foobar")
    product1 = es_mixer.blend('product', id=2, title="Barfoo")

    req = RequestFactory().get('/')
    resp = views.search_view(req, search="Foobar")
    assert len(resp) == 1, 'Finds only one item that has Foobar in the title'
    assert resp[0].title == 'Foobar', 'Finds the item we searched for'

    # You can also update an existing document
    product1 = es_mixer.update('product', id=1, title="New Title", published=False)
    resp = views.search_view(req, search="Foobar")
    assert len(resp) == 0, (
      'Finds zero items, because no item has Foobar in the title any more')
```

Big word of warning: We are no ES experts. We have only started using ES around
June 2019 and one of the first problems that we had was that we did not know how
to properly write unittests for our Django views and Graphene resolver
functions. There are probably much better ways to do this. If you know one, we
would love to hear about it (just open an issue and tell us about it!).

# Installation

```
pip install elasticsearch-features
```

# TODO

- How to make sure that ES is empty at the beginning of each test?
