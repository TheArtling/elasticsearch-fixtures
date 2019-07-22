import requests


class ESMixer:

    def __init__(self, host):
        """
        Initializes an ESMixer instance.

        :host: Hostname of your Elasticsearch instance with trailing slash
        :index: Name of the index in your Elasticsearch instance where mixer
          will save the test-fixtures.

        """
        self.host = host

    def wipe_index(self, index):
        """
        Deletes all documents in the given index.

        :index: String representing the index that should be deleted.

        """
        url = f'{self.host}{index}/_delete_by_query?conflicts=proceed'
        data = {'query': {'match_all': {}}}
        resp = requests.post(url, json=data)
        return resp.json()

    def get(self, index, id):
        """
        Returns the given document for the given index.

        """
        url = f'{self.host}{index}/_doc/{id}'
        resp = requests.get(url)
        return resp.json()

    def blend(self, index, id=None, **kwargs):
        """
        Creates or replaces the given document in the index.

        :index: String representing the index where the document should be
          created.
        :id: The id of the document. If a document with this id already exists,
          the existing document will be replaced, otherwise a new document will
          be created. If no id is given, a new document will be created and a
          new id will be auto-created.

        """
        url = f'{self.host}{index}/_doc/'
        method = 'post'
        if id is not None:
            method = 'put'
            url += id
        resp = getattr(requests, method)(url, json=kwargs)
        _id = resp.json()['_id']
        return self.get(index, _id)

    def update(self, index, id, **kwargs):
        """
        Performs a partial update for an existing document in the index.

        :index: String representing the index where the document should be
          updated.
        :id: The id of the document that shall be updated.

        """
        url = f'{self.host}{index}/_doc/{id}/_update'
        data = {'doc': {**kwargs}}
        requests.post(url, json=data)
        return self.get(index, id)
