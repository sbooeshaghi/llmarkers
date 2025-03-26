## ADAPTED FROM ../analysis/llm_extract.ipynb

"""
This script prompts the user to entire a file name and iterates through the annotated evidence human 
to find source rationales and uses LLama3.2 to extract cell type-marker gene pairs from each detected 
source rationale.
"""
import json
import pandas as pd
from pydantic import BaseModel, Field
from typing import List, Optional
from ollama import chat
import os

# Permissive class object (allows for missing fields)
class MarkerGene(BaseModel):
    marker_gene_name: Optional[str] = Field(
        None, 
        description="The name of the marker gene that is associated with a specific cell type."
    )
    cell_type_name: Optional[str] = Field(
        None, 
        description="The name of the cell type for which this gene serves as a marker."
    )

class MarkerGeneList(BaseModel):
    genes: List[MarkerGene]  # A list of marker genes extracted from the input text

# Restrictive class object does not allow for missing fields
class MarkerGeneStrict(BaseModel):
    marker_gene_name: str = Field(
        ..., 
        description="The name of the marker gene that is associated with a specific cell type."
    )
    cell_type_name: str = Field(
        ..., 
        description="The name of the cell type for which this gene serves as a marker."
    )

class MarkerGeneListStrict(BaseModel):
    genes: List[MarkerGeneStrict]  # A list of marker genes extracted from the input text

MODEL_TO_USE = "llama3.2"

LLMODELS = {
    "deepseek-r1": "deepseek-r1",
    "llama3.2": "llama3.2",
    "llama3.3": "llama3.3"
}

DATA_MODELS = {
    "MarkerGeneListStrict": MarkerGeneListStrict,
    "MarkerGeneStrict": MarkerGeneStrict
}

system_prompt = """
You are an expert in genomics analyzing scientific literature to extract marker genes for different cell types. 

Your goal is to identify and structure marker gene data from the given text. For each marker gene mentioned, extract:
- The **gene name** (marker_gene_name).
- The **cell type** it is associated with (cell_type_name).

The data must be extracted as written in the text, without any modifications.

Return the results in **structured JSON format** with the following schema:
{
    "genes": [
        {
            "cell_type_name": "Neuron",
            "marker_gene_name": "GeneX",
        },
        ...
    ]
}
"""

def extract_genes(user_prompt, system_prompt, data_model, model=MODEL_TO_USE):
    response = chat(
        messages=[
            {
                'role': 'system',
                'content': system_prompt,
            },
            {
                'role': 'user',
                'content': user_prompt,
            }
        ],
        model = model,
        format = data_model.model_json_schema(),
        options={'temperature': 0},  # Make responses more deterministic

    )
    genes = data_model.model_validate_json(response.message.content)
    return genes.model_dump()["genes"]

def load_evidence(fn, ds_name):
    ## from llm_extract.ipynb
    df = pd.read_json(fn)
    # Unwrap the 'source' column (contains a dictionary) into separate columns
    source_df = df['source'].apply(pd.Series)
    extracted_df = df['extracted'].apply(pd.Series).add_prefix('extracted_')
    # Combine the original DataFrame with the unwrapped columns
    df = pd.concat([df.drop(columns=['source', 'extracted']), source_df, extracted_df], axis=1)
    df["ds"] = ds_name
    del df["derived"]
    return df

def get_llm_evidence(folder_name):
    fn = os.path.join(folder_name, "evidence_human", "evidence.json")
    ds_name = folder_name
    df = load_evidence(fn, ds_name)

    model_metadata = {
        "model_id" : LLMODELS[MODEL_TO_USE],
        "system_prompt": system_prompt,
        "data_model": DATA_MODELS["MarkerGeneListStrict"].__name__
    }

    ## get all the unique source rationales by querying the dataframe for source_rationales where source_type is text
    tdf = df.query("source_type == 'text'").copy()
    uniq_src = tdf.source_rationale.unique()
    ct_mgs = []

    for idx, text in enumerate(uniq_src):
        print(f"{idx + 1}/{len(uniq_src)}")
        ct_mg = extract_genes(text, model_metadata["system_prompt"], DATA_MODELS[model_metadata["data_model"]], model=model_metadata["model_id"])
    
        if len(ct_mg) == 0:
            continue
        
        for g in ct_mg:
            tmp = {
                "extracted": {
                    "organism": "homo_sapiens",
                    "cell_type_label": g["cell_type_name"],
                    "cell_source": None,
                    "cell_state": None,
                    "feature_name": g["marker_gene_name"],
                    "feature_type": "gene",
                },
                "derived": {
                    "organism": "homo_sapiens",
                    "cell_type_id": None,
                    "cell_type_label": g["cell_type_name"],
                    "cell_source": None,
                    "cell_state": None,
                    "feature_name": g["marker_gene_name"],
                    "feature_type": "gene",
                    "feature_identifier": None,
                    "feature_identifier_type": None,
                },
                "source": {
                    "source_type": "text",
                    "source_rationale": text,
                    "source_id": "text"
                }
            }

            ct_mgs.append(tmp)

    llm_folder = os.path.join(folder_name, f"evidence_llm_{MODEL_TO_USE}")
    os.mkdir(llm_folder)
    llm_fn = os.path.join(llm_folder, "evidence.json") 
    with open(llm_fn, 'w') as f:
        json.dump(ct_mgs, f, indent = 4)
    model_fn = os.path.join(llm_folder, "model_metadata.json")
    with open(model_fn, 'w') as f:
        json.dump(model_metadata, f, indent = 4)
    print("Done!")

# user functionality: 
fn = input("Enter folder name: ")
get_llm_evidence(fn)


