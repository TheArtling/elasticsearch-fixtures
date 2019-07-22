import requests


class ESMixer:

    def __init__(self, host, index):
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

    def blend(self, index, id, **kwargs):
        """
        Creates or replaces the given document in the index.

        :index: String representing the index where the document should be
          created.
        :id: The id of the document. If a document with this id already exists,
          the existing document will be replaced, otherwise a new document will
          be created.

        """
        url = f'{self.host}{index}/_doc/{id}'
        data = kwargs
        resp = requests.put(url, json=data)
        return resp.json()

    def update(self, index, id, **kwargs):
        """
        Performs a partial update for an existing document in the index.

        :index: String representing the index where the document should be
          updated.
        :id: The id of the document that shall be updated.

        """
        url = f'{self.host}{index}/_doc/{id}/_update'
        data = {'doc': {**kwargs}}
        resp = requests.post(url, json=data)
        return resp.json()
