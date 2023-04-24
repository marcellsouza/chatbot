import requests
from api.models import *
import meilisearch
class Api:
    def __init__(self,endpoint='/cms/servicos'):
        self.baseurl = 'https://facil.prodap.ap.gov.br/api'
        if endpoint:
            self.baseurl += endpoint
        self.headers = {'Authorization' : 'Api-Key wPoh9cBR.eJoyhYljQPATWZhLY0gp8l58Cl4zD5uL'}

    def __request(self,params,endpoint=None):
        url = self.baseurl
        if endpoint:
            url += endpoint
        req = requests.get(url, params=params, headers=self.headers)
        return req.json()

    def search(self, term):
        params = { 'search' : term, 'ativo'  : 'true' }
        response =  self.__request(params)
        if response['results']:
            services = [ Service(serv) for serv in response['results'] ]
            return services
        else:
            return []

    def view(self, link):
        params = { 'slug' : link}
        response = self.__request(params)
        full_article = response['results'][0]
        return Article(full_article)

class Meili:
    def __init__(self,index,key=None):
        self.client = meilisearch.Client('http://apicache_meili:7700', key)
        self.meili = self.client.index(index)

    def search(self, term, first=False,hits=5):
        results = self.meili.search(term)
        if len(results['hits']) > 0:
            if(first):
                return results['hits'][0]
            else:
                return results['hits'][:hits]
        else:
            return []


