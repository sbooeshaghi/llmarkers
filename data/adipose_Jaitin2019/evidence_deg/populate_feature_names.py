import json

class EnsemblIdFinder:

    def __init__(self):
        gtf_fn = "/Users/nithya/Homo_sapiens.GRCh38.113.gtf"
        self.gene_data = {}
        self.create_mapping(gtf_fn)
        
        
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
                    self.gene_data[gene_id] = gene_name
    
    def update_json(self, json_fn = 'evidence.json'):
        with open(json_fn, 'r') as file:
            data = json.load(file)
        species = 'human'
        
        for obj in data:
            obj_keys = obj.keys()
            main_obj = obj['derived']
            
            ensembl_id = main_obj['feature_identifier']

            if ensembl_id in self.gene_data.keys():
                gene = self.gene_data[ensembl_id]
                main_obj['feature_name'] = gene
                obj['extracted']['feature_name'] = gene

            else:
                print(main_obj)

        with open(json_fn, "w") as file:
            json.dump(data, file, indent = 4)
        
eif = EnsemblIdFinder()
eif.update_json("evidence_unfiltered.json")
