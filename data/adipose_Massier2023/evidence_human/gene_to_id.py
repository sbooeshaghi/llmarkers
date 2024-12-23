#!/usr/bin/env python

import sys
import json
import time

# Python 2/3 adaptability

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

# ADAPTED FROM: https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client 

class EnsemblRestClient(object):
    def __init__(self, server='http://rest.ensembl.org', reqs_per_sec=5):
        self.server = server
        self.reqs_per_sec = reqs_per_sec
        self.req_count = 0
        self.last_req = 0

    def perform_rest_action(self, endpoint, hdrs=None, params=None):
        if hdrs is None:
            hdrs = {}

        if 'Content-Type' not in hdrs:
            hdrs['Content-Type'] = 'application/json'

        if params:
            endpoint += '?' + urlencode(params)

        data = None

        # check if we need to rate limit ourselves
        if self.req_count >= self.reqs_per_sec:
            delta = time.time() - self.last_req
            if delta < 1:
                time.sleep(1 - delta)
            self.last_req = time.time()
            self.req_count = 0
        
        try:
            request = Request(self.server + endpoint, headers=hdrs)
            response = urlopen(request)
            content = response.read()
            if content:
                data = json.loads(content)
            self.req_count += 1

        except HTTPError as e:
            # check if we are being rate limited by the server
            if e.code == 429:
                if 'Retry-After' in e.headers:
                    retry = e.headers['Retry-After']
                    time.sleep(float(retry))
                    self.perform_rest_action(endpoint, hdrs, params)
            else:
                sys.stderr.write('Request failed for {0}: Status code: {1.code} Reason: {1.reason}\n'.format(endpoint, e))
           
        return data

    def get_id(self, species, symbol):
        genes = self.perform_rest_action(
            endpoint='/xrefs/symbol/{0}/{1}'.format(species, symbol), 
            params={'object_type': 'gene'}
        )
        if genes:
            stable_id = genes[0]['id']
            return stable_id
        else:
            return "gene not found"


def run(species, symbol):
    client = EnsemblRestClient()
    gene_id = client.get_id(species, symbol)
    return gene_id

if __name__ == '__main__':
    with open('evidence.json', 'r') as file:
        data = json.load(file)
    for obj in data:
        species = obj['extracted']['organism']
        if species == 'mus_musculus':
            species = 'mouse'
        else:
            species = 'human'
        symbol = obj['derived']['gene']
        if symbol.isascii():
            gene_id = run(species, symbol)
        
            if gene_id is not None:
                if gene_id == "gene not found":
                    print(obj)
                else:
                    obj['derived']['gene_id'] = gene_id
        else:
            print(obj)

    with open("evidence.json", "w") as file:
        json.dump(data, file, indent = 4)

    print("Done editing!")