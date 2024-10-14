#!/usr/bin/env python3

import pandas as pd
import sys

print(sys.argv)
df = pd.read_json(sys.argv[1])
d = df.groupby("cell_type")["gene"].apply(list).to_dict()


def write_dict(fname, d):
    with open(fname, "w") as f:
        for key, values in d.items():
            # Write the key
            f.write(f"{key}\t")
            # Write the values as a comma-separated list
            f.write(",".join(values) + "\n")


write_dict(sys.argv[2], d)
