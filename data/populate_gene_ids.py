import json

import sys
import json
import time

# Python 2/3 adaptability

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

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

class EnsemblIdFinder:

    def __init__(self):
        gtf_fn = "/Users/nithya/Homo_sapiens.GRCh38.113.gtf"
        self.gene_data = {}
        self.create_mapping(gtf_fn)
        self.client = EnsemblRestClient()
        
    def create_mapping(self,gtf_file):
        # open the file
        with open(gtf_file, 'r') as file:
            # now, we want to go through every line in the file
            for line in file:
                if line.startswith('#'):
                    continue # skip comment lines in the gtf file
                columns = line.strip().split('\t') # get all the diff columns within gtf file 
                if columns[2] == 'gene':
                    gene_details = columns[8].split(';')
                    gene_id = ""
                    gene_name = ""
                    for detail in gene_details:
                        detail = detail.strip();
                        if detail.startswith("gene_id"):
                            gene_id_arr = detail.split(' ') # this gives the label and the id
                            gene_id = gene_id_arr[1].strip('"') # remove the double quotes surrounding the gene id
                        elif detail.startswith("gene_name"):
                            gene_id_arr = detail.split(' ')
                            gene_name = gene_id_arr[1].strip('"')
                if gene_name and gene_id:
                    self.gene_data[gene_name] = gene_id
    
    def update_json(self, json_fn = 'evidence.json'):
        with open(json_fn, 'r') as file:
            data = json.load(file)
        
        for obj in data:
            obj_keys = obj.keys()
            main_obj = obj
            species = 'human'

            if 'extracted' in obj_keys and obj['extracted']['organism'] == 'mus_musculus':
                species = obj['extracted']['organism']
            elif obj['organism'] == 'mus_musculus':
                    species = obj['organism']

            if species == 'human':
                if 'derived' in obj_keys:
                    main_obj = obj['derived']

                gene = main_obj['gene']

                if gene in self.gene_data.keys():
                    gene_id = self.gene_data[gene]
                    main_obj['gene_id'] = gene_id
                else:
                    result = self.client.get_id(species, gene) # 2nd pass is using the Ensebml REST API
                    if result == "gene not found":
                        if "." in main_obj['gene']:
                            first_part = main_obj['gene'].split(".")[0]
                            print(first_part)
                            if first_part in self.gene_data.keys():
                                gene_id = self.gene_data[first_part]
                                main_obj['gene_id'] = gene_id
                            else:
                                result = self.client.get_id(species, gene) # 2nd pass is using the Ensebml REST API
                                if result == "gene not found":
                                    print(obj)
                                else:
                                    main_obj['gene_id'] = result
                        else:
                            print(obj)
                    else:
                        main_obj['gene_id'] = result

        with open(json_fn, "w") as file:
            json.dump(data, file, indent = 4)
        
eif = EnsemblIdFinder()
eif.update_json("adipose_Hildreth2021/evidence_deg/evidence.json")
