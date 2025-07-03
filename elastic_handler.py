# builtins
import logging
import os
import datetime
import sys
import elasticsearch 
from elasticsearch.helpers import bulk

ELASTIC_HOST = os.environ.get("INPUT_ELASTIC_HOST")
ELASTIC_USERNAME = os.environ.get("INPUT_ELASTIC_USERNAME")
ELASTIC_PASSWORD = os.environ.get("INPUT_ELASTIC_PASSWORD")
ELASTIC_INDEX = os.environ.get("INPUT_ELASTIC_INDEX")

try:
    assert ELASTIC_HOST not in (None, '')
except:
    output = "The input ELASTIC_HOST is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    assert ELASTIC_USERNAME not in (None, '')
except:
    output = "The input ELASTIC_USERNAME is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    assert ELASTIC_PASSWORD not in (None, '')
except:
    output = "The input ELASTIC_PASSWORD is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    assert ELASTIC_INDEX not in (None, '')
    now = datetime.datetime.now()
    elastic_index = f"{ELASTIC_INDEX}-{now.month}-{now.day}"


except:
    output = "The input ELASTIC_INDEX is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    es = elasticsearch.Elasticsearch(
        ELASTIC_HOST,
        http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
    )
    if es.ping():
        print("connected to Elasticsearch.")
    if not es.ping():
        print("Failed to connect to Elasticsearch.")

except elasticsearch.exceptions.AuthorizationException as exc:
    output = "Authentication to elastic failed"
    print(f"Error: {output}")
    sys.exit(-1)


class ElasticHandler(logging.Handler):
    def __init__(self, *args, **kwargs):
        super(ElasticHandler, self).__init__(*args, **kwargs)
        self.buffer = []

    def emit(self, record):
        try:
            es = elasticsearch.Elasticsearch(
                ELASTIC_HOST,
                http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
            )
            record_dict = record.__dict__
            record_dict["@timestamp"] = int(record_dict.pop("created") * 1000)
            self.buffer.append({
                "_index": elastic_index,
                **record_dict
            })
        except ValueError as e:
            output = f"Error inserting to Elastic {str(e)}"
            print(f"Error: {output}")
            print(f"::set-output name=result::{output}")
            return

    def flush(self):
        print("it runs to flush.")
        es = elasticsearch.Elasticsearch(
            ELASTIC_HOST,
            http_auth=(ELASTIC_USERNAME, ELASTIC_PASSWORD)
        )
        # if the index is not exist, create it with mapping:
        if not es.indices.exists(index=elastic_index):
            print(es.info())
            mapping = '''
            {  
              "mappings":{  
                  "properties": {
                    "@timestamp": {
                      "type":   "date",
                      "format": "epoch_millis"
                    }
                  }
                }
            }'''
            es.indices.create(index=elastic_index, body=mapping)
            print("indice:", es.indices)

        #Bulking to Elasticsearch Cluster
        success, failure = bulk(
            client=es,
            actions=self.buffer
        )
        # Check if any failures occurred
        if failure:
            print(f"Bulk operation failed with {len(failure)} failures.")
            for fail in failure:
                print(f"Failure: {fail}")
        else:
            print("Bulk operation succeeded.")

            print(f"Successfully indexed {success} logs to Elasticsearch.")
        
