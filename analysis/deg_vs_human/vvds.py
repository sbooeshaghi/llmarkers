import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

class VVD:
    def __init__(self, articles):
        self.articles = articles
        
    
    def display(self):
        x_axis = [x.xa for x in self.articles]
        y1 = [x.y1 for x in self.articles]
        y2 = [x.y2 for x in self.articles]
        y3 = [x.y3 for x in self.articles]

        plt.title("Vertical Venn Diagram showing Left Difference (Red), Intersection (Blue), and Right Difference (Green) between Evidence Human and Evidence DEG")

        plt.bar(x_axis, y1, color = 'r')
        plt.bar(x_axis, y2, bottom = y1, color = 'b')
        plt.bar(x_axis, y3, bottom = y2, color = 'g')

        plt.show()
    
class Article:
    def __init__(self, name, deg_fn, human_fn):
        derived_human_ev = self.load_human_evidence(human_fn)
        deg_ev = self.load_deg_evidence(deg_fn)

        feature = "cell_type_label" # eventually change this to comparing based on a map we can create

        first = derived_human_ev[feature].str.strip().str.upper().unique()
        first = self.get_standard_labels(first)
        second = deg_ev[feature].str.strip().str.upper().unique()
        second = self.get_standard_labels(second)

        left  = self.set_diff(first, second)
        itx   = self.set_itx(first, second)
        right = self.set_diff(second, first)

        self.y1 = left
        self.y2 = itx
        self.y3 = right
        self.xa = name

    def load_human_evidence(self, fn):
        # we only want derived since we're going to compare gene ids
        df = pd.read_json(fn)
        derived_df = df['derived'].apply(pd.Series)
        return derived_df

    def load_deg_evidence(self, fn):
        df = pd.read_json(fn)
        df = df.apply(pd.Series)
        return df
    
    def set_itx(self, a, b):
        return np.intersect1d(a, b).shape[0]
    
    def set_diff_vals(self, a,b):
        return np.setdiff1d(a,b)
    
    def set_diff(self, a, b):
        return self.set_diff_vals(a,b).shape[0]
    
    def get_standard_labels(self, labels):
        """
        Returns the standardized labels of cell type labels using a global map
        """
        with open('cell_type_label_map.json', 'r') as file:
            map_dict = json.load(file)
            corrected_labels = []
            for l in list(map(str.upper,labels)):
                added = False
                for key, vals in map_dict.items():
                    if l in vals or l == key:
                        corrected_labels.append(key)
                        added = True
                if not added:
                    corrected_labels.append(l)
        return np.array(corrected_labels)

hildreth_unfiltered = Article("Hildreth Unfiltered", "../../data/adipose_Hildreth2021/evidence_deg/evidence_unfiltered.json", "../../data/adipose_Hildreth2021/evidence_human/evidence.json")
hildreth_filtered = Article("Hildreth Filtered", "../../data/adipose_Hildreth2021/evidence_deg/evidence.json", "../../data/adipose_Hildreth2021/evidence_human/evidence.json")
emont_unfiltered = Article("Emont Unfiltered", "../../data/adipose_Emont2022/evidence_deg/evidence_unfiltered.json", "../../data/adipose_Emont2022/evidence_human/evidence.json")
emont_filtered = Article("Emont Filtered", "../../data/adipose_Emont2022/evidence_deg/evidence.json", "../../data/adipose_Emont2022/evidence_human/evidence.json")

vvd = VVD([hildreth_filtered, hildreth_unfiltered, emont_filtered, emont_unfiltered])
vvd.display()