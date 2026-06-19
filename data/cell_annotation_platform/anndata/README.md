# CAP AnnData Inputs

The CAP liver expression analysis in `analysis/build_cap_liver_local_global_deg.py`
uses two Cell Annotation Platform AnnData files. These files are large local
inputs and are intentionally not tracked in git. Download them into this
directory before rerunning the CAP liver panels.

| Local file | CAP dataset | Source URL | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| `cap_1437_liver_all_cells.h5ad` | project 618, dataset 1437, all cells from human liver dataset | `https://storage.googleapis.com/cap-gke-prod-anndata/public-anndata-project_569_1__published__-iEDNQN_ll_FzAv9xecdC_1437.h5ad` | 1655014011 | `44dc27f42ad710631432f6de4015b6e7135dea269aa4ceb6924b843b7a443ee4` |
| `cap_1440_liver_myeloid.h5ad` | project 618, dataset 1440, myeloid cells from human liver dataset | `https://storage.googleapis.com/cap-gke-prod-anndata/public-anndata-project_569_1__published__0s70XkvGftSFKbcb1pEH6_1440.h5ad` | 449594306 | `f3262182ee91ef909f9545c40b4bc9166616f3d436dfd012b1102413857c6a85` |

Example rebuild:

```bash
curl -L "https://storage.googleapis.com/cap-gke-prod-anndata/public-anndata-project_569_1__published__-iEDNQN_ll_FzAv9xecdC_1437.h5ad" -o data/cell_annotation_platform/anndata/cap_1437_liver_all_cells.h5ad
curl -L "https://storage.googleapis.com/cap-gke-prod-anndata/public-anndata-project_569_1__published__0s70XkvGftSFKbcb1pEH6_1440.h5ad" -o data/cell_annotation_platform/anndata/cap_1440_liver_myeloid.h5ad
shasum -a 256 data/cell_annotation_platform/anndata/cap_1437_liver_all_cells.h5ad data/cell_annotation_platform/anndata/cap_1440_liver_myeloid.h5ad
```

Then run:

```bash
uv run --locked python analysis/build_cap_liver_local_global_deg.py
```
