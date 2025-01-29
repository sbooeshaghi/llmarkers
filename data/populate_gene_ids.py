import pandas as pd

class EnsemblIdFinder:

    def __init__(self,paper_name, json_fn = "evidence.json"):
        self.paper_name = paper_name
        self.json_fn = json_fn
        gtf_fn = "/Users/nithya/Homo_sapiens.GRCh38.113.gtf"

        col_names = ["seqname", "source", "feature", "start", "end", "score", 
                 "strand", "frame", "attribute"]
        
        
        
       
eif = EnsemblIdFinder("eg_paper")
