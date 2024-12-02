import numpy as np
import pandas as pd

def load_evidence(fn):
    df = pd.read_json(fn)
    # Unwrap the 'source' column (contains a dictionary) into separate columns
    source_df = df['source'].apply(pd.Series)
    extracted_df = df['extracted'].apply(pd.Series).add_prefix('extracted_')
    derived_df = df['derived'].apply(pd.Series).add_prefix('derived_')
    # Combine the original DataFrame with the unwrapped columns
    df = pd.concat([df.drop(columns=['source', 'extracted', 'derived']), source_df, extracted_df, derived_df], axis=1)
    return df

def make_comparison(paper1: str, paper2: str):
    """
    Finds similarites in gene expression between all cells mentioned in two papers and returns a 3D matrix describing the left difference, intersection, and right difference in gene expression.

    Args:
        paper1 (str): the file name of the first paper
        paper2 (str): the file name of the second paper
    
    Returns:
        list: the 3D matrix describing set difference and intersection in gene expression
    """
    """
    data1 = load_evidence(paper1)
    data2 = load_evidence(paper2)
    set_arr = [1,2,3] # placeholder
    
    feature = 'derived_cell_type_label'
    #print(data1[feature].to_string(index=False).upper())
    

    data = {'x': data1[feature].to_string(index=False).upper(), 'y': data2[feature].to_string(index=False).upper(), 'z': set_arr}
    df = pd.DataFrame(data)
    return df
    """
    

    data1 = load_evidence(paper1)
    data2 = load_evidence(paper2)
    
    feature = 'derived_cell_type_label'
    
    # Extract unique x (rows) and y (columns)
    x_labels = sorted(data1[feature].unique())
    y_labels = sorted(data2[feature].unique())

    result_df = pd.DataFrame(index = x_labels, columns=y_labels, dtype=object)
    
    for x in x_labels:
        for y in y_labels:
            genes1 = set(data1[data1[feature] == x]['derived_gene'])
            genes2 = set(data2[data2[feature] == y]['derived_gene'])

            left_diff = genes1 - genes2
            intersection = genes1 & genes2
            right_diff = genes2 - genes1

            result_df.loc[x,y] = [left_diff, intersection, right_diff]

    return result_df

f1_fn = "../data/adipose_Emont2022/evidence_human/evidence.json"
f2_fn = "../data/adipose_Vijay2019/evidence_human/evidence.json"

make_comparison(f1_fn, f2_fn)

