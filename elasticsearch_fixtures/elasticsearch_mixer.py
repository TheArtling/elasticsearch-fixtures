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
        self.index = index

    def wipe_index(self):
        """
        Deletes all documents in the given index.

        """
        url = f'{self.host}{self.index}/_delete_by_query?conflicts=proceed'
        data = {'query': {'match_all': {}}}
        resp = requests.post(url, json=data)
        return resp

    def blend(self):
        pass