from urllib3.exceptions import InsecureRequestWarning
import urllib3
from elasticsearch import Elasticsearch
import warnings


class ESearch():

    def __init__(self, host='elastic', password='1D+eJ1FMf71gUJHx85Mi'):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        urllib3.disable_warnings(InsecureRequestWarning)
        self.es = Elasticsearch(["https://localhost:9200"], http_auth=(host, password) ,verify_certs=False)

    def fuzzy_search(self, query, fuzziness, result_size):
        search_body = {
            "size": result_size,
            "query": {
                "fuzzy": {
                    'text': {
                        "value": query,
                        "fuzziness": fuzziness
                    }
                }
            }
        }

        response = self.es.search(index='tweets', body=search_body)
        id_list = []
        for i, hit in enumerate(response['hits']['hits']):
            id_list.append(hit['_id'])
            print(f"{i}: ID: {hit['_id']}, Score: {hit['_score']}, Text: {hit['_source']['text']}")
        
        return id_list
    
        
    def full_text_search(self, query, result_size):
        search_body = {
            "size": result_size,
            "query": {
                "match": {
                    'text': query
                }
            }
        }

        response = self.es.search(index='tweets', query=search_body)
        id_list = []
        for i, hit in enumerate(response['hits']['hits']):
            id_list.append(hit['_id'])
            print(f"{i}: ID: {hit['_id']}, Score: {hit['_score']}, Text: {hit['_source']['text']}")

        return id_list


    def text_search(self, query, fuzziness=2, result_size=5):
        if len(query.split()) > 1:
            return self.full_text_search(query, result_size)
        else:
            return self.fuzzy_search(query, fuzziness, result_size)


    def search_text_from_id(self, tweet_id):
        record = self.es.get(index='tweets', id=tweet_id)
        return record['_source']['text']


if __name__ == '__main__':
    es = ESearch()
    print(es.search_text_from_id('1254022770679320576'))

