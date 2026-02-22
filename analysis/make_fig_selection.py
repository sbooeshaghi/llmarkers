"""Generate Figure 3: LLM marker selection analysis.

Three panels:
  (a) Selection pair F1 vs top-N DEGs (named + anon + upper bound recall)
  (b) Per-dataset comparison of extraction, generation, selection (pair F1)
  (c) Performance vs cost across methods

All methods evaluated against text-sourced human annotations only.
"""

import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# ── Config ───────────────────────────────────────────────────────────
fsize = 10
plt.rcParams.update({"font.size": fsize})
FIG_DIR = Path(__file__).resolve().parent / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

datasets = [
    "adipose_Emont2022",
    "adipose_Hildreth2021",
    "bone_He2021",
    "eye_Gautam2021",
    "lung_Adams2020",
    "ovary_Wagner2020",
    "testis_Shamis2020",
]
labels = {
    "adipose_Emont2022": "Adipose\n(Emont)",
    "adipose_Hildreth2021": "Adipose\n(Hildreth)",
    "bone_He2021": "Bone\n(He)",
    "eye_Gautam2021": "Eye\n(Gautam)",
    "lung_Adams2020": "Lung\n(Adams)",
    "ovary_Wagner2020": "Ovary\n(Wagner)",
    "testis_Shamis2020": "Testis\n(Shamis)",
}
short_labels = {
    "adipose_Emont2022": "Emont",
    "adipose_Hildreth2021": "Hildreth",
    "bone_He2021": "He",
    "eye_Gautam2021": "Gautam",
    "lung_Adams2020": "Adams",
    "ovary_Wagner2020": "Wagner",
    "testis_Shamis2020": "Shamis",
}
N_values = [10, 20, 30, 40, 50, 100, 200, 300, 400, 500]

# ── Helpers ──────────────────────────────────────────────────────────
def load_and_norm(path):
    df = pd.read_json(path)
    df["group_name"] = df["group_name"].str.strip().str.upper()
    df["feature_name"] = df["feature_name"].str.strip().str.upper()
    return df

def build_pairs(df, col="feature_id"):
    pairs = set()
    for _, r in df.iterrows():
        gn, fv = r.get("group_name"), r.get(col)
        if pd.notna(gn) and pd.notna(fv) and gn and fv:
            pairs.add((gn, fv))
    return pairs

def build_groups(df, col="feature_id"):
    groups = {}
    for _, r in df.iterrows():
        gn, fv = r.get("group_name"), r.get(col)
        if pd.notna(gn) and pd.notna(fv) and gn and fv:
            groups.setdefault(gn, set()).add(fv)
    return groups

def pair_metrics(pairs_a, pairs_b):
    if not pairs_a and not pairs_b:
        return 0, 0, 0
    tp = len(pairs_a & pairs_b)
    p = tp / len(pairs_a) if pairs_a else 0
    r = tp / len(pairs_b) if pairs_b else 0
    f = 2 * p * r / (p + r) if (p + r) > 0 else 0
    return p, r, f

def per_celltype_gene_f1(groups_a, groups_b):
    shared = set(groups_a) & set(groups_b)
    if not shared:
        return 0, 0
    f1s = []
    for ct in shared:
        a, b = groups_a[ct], groups_b[ct]
        tp = len(a & b)
        p = tp / len(a) if a else 0
        r = tp / len(b) if b else 0
        f = 2 * p * r / (p + r) if (p + r) > 0 else 0
        f1s.append(f)
    return np.mean(f1s), len(shared)

def upper_bound_recall(hmn_pairs, deg_df, top_n):
    deg_top = deg_df[deg_df["metrics_rank"] <= top_n]
    deg_pairs = build_pairs(deg_top)
    if not hmn_pairs:
        return 0
    return len(hmn_pairs & deg_pairs) / len(hmn_pairs)

# ── Load data ────────────────────────────────────────────────────────
data = {}
for ds in datasets:
    base = Path(f"../data/{ds}")
    hmn_all = load_and_norm(base / "evidence_human" / "extracted.json")
    hmn = hmn_all[hmn_all["source_type"] == "text"].copy()
    deg = load_and_norm(base / "evidence_deg" / "extracted.json")
    gen = load_and_norm(base / "evidence_generated" / "extracted.json")
    llm = load_and_norm(base / "evidence_llm" / "extracted_txt.json")

    sel, sel_anon = {}, {}
    for n in N_values:
        p = base / "evidence_selected" / f"selected_top{n}.json"
        if p.exists():
            sel[n] = load_and_norm(p)
        pa = base / "evidence_selected" / f"selected_anon_top{n}.json"
        if pa.exists():
            sel_anon[n] = load_and_norm(pa)

    data[ds] = {"hmn": hmn, "deg": deg, "gen": gen, "llm": llm, "sel": sel, "sel_anon": sel_anon}

# ── Compute sweep metrics ────────────────────────────────────────────
sweep_rows = []
for ds in datasets:
    d = data[ds]
    hmn_pairs = build_pairs(d["hmn"])
    hmn_groups = build_groups(d["hmn"])
    for mode, sel_dict in [("named", d["sel"]), ("anon", d["sel_anon"])]:
        for n in N_values:
            if n not in sel_dict:
                continue
            sel_pairs = build_pairs(sel_dict[n])
            sel_groups = build_groups(sel_dict[n])
            p_prec, p_rec, p_f1 = pair_metrics(sel_pairs, hmn_pairs)
            ct_f1, _ = per_celltype_gene_f1(sel_groups, hmn_groups)
            ub = upper_bound_recall(hmn_pairs, d["deg"], n)
            sweep_rows.append({
                "dataset": ds, "mode": mode, "N": n,
                "pair_precision": p_prec, "pair_recall": p_rec, "pair_f1": p_f1,
                "gene_f1": ct_f1, "upper_bound_recall": ub,
            })
sweep = pd.DataFrame(sweep_rows)

# ── Compute method comparison ────────────────────────────────────────
named = sweep[sweep["mode"] == "named"]
best_named = named.loc[named.groupby("dataset")["pair_f1"].idxmax()]

method_rows = []
for ds in datasets:
    d = data[ds]
    hmn_pairs = build_pairs(d["hmn"])
    hmn_groups = build_groups(d["hmn"])

    ext_p, ext_r, ext_f1 = pair_metrics(build_pairs(d["llm"]), hmn_pairs)
    gen_p, gen_r, gen_f1 = pair_metrics(build_pairs(d["gen"]), hmn_pairs)
    bn = best_named[best_named["dataset"] == ds].iloc[0]

    method_rows.append({
        "dataset": ds,
        "ext_pair_f1": ext_f1,
        "gen_pair_f1": gen_f1,
        "sel_pair_f1": bn["pair_f1"],
    })
methods = pd.DataFrame(method_rows)

# ── Cost data ────────────────────────────────────────────────────────
# Extraction costs
ext_cost = 0
for ds in datasets:
    mf = Path(f"../data/{ds}/evidence_llm/metrics.json")
    if mf.exists():
        m = json.load(open(mf))
        ext_cost += m.get("total_cost", 0)

# Generation costs
gen_cost = 0
for ds in datasets:
    mf = Path(f"../data/{ds}/evidence_generated/metrics.json")
    if mf.exists():
        m = json.load(open(mf))
        gen_cost += m.get("total_cost", 0)

# Selection costs (at best N per dataset)
sel_cost = 0
for ds in datasets:
    bn = best_named[best_named["dataset"] == ds].iloc[0]
    best_n = int(bn["N"])
    mf = Path(f"../data/{ds}/evidence_selected/metrics_top{best_n}.json")
    if mf.exists():
        m = json.load(open(mf))
        sel_cost += m.get("total_cost", 0)

# ── Figure ───────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), constrained_layout=True)

# ── Panel (a): Selection sweep ───────────────────────────────────────
ax = axes[0]
named_mean = sweep[sweep["mode"] == "named"].groupby("N").mean(numeric_only=True).reset_index()
anon_mean = sweep[sweep["mode"] == "anon"].groupby("N").mean(numeric_only=True).reset_index()

ax.plot(named_mean["N"], named_mean["pair_f1"], "o-", color="tab:blue",
        label="Named", markersize=5, linewidth=1.5)
ax.plot(anon_mean["N"], anon_mean["pair_f1"], "s-", color="tab:red",
        label="Anonymous", markersize=5, linewidth=1.5)
ax.plot(named_mean["N"], named_mean["upper_bound_recall"], "^--", color="gray",
        alpha=0.6, label="Upper bound recall", markersize=5, linewidth=1)

# Add generation baseline
gen_mean_f1 = methods["gen_pair_f1"].mean()
ax.axhline(gen_mean_f1, color="tab:orange", linestyle=":", linewidth=1.5,
           label=f"Generation (F1={gen_mean_f1:.2f})", alpha=0.8)

# Add extraction baseline
ext_mean_f1 = methods["ext_pair_f1"].mean()
ax.axhline(ext_mean_f1, color="tab:green", linestyle=":", linewidth=1.5,
           label=f"Extraction (F1={ext_mean_f1:.2f})", alpha=0.8)

ax.set_xlabel("Top N DEGs per cell type")
ax.set_ylabel("Pair F1")
ax.set_title("(a) Selection performance vs. N")
ax.set_xscale("log")
ax.set_xticks(N_values)
ax.set_xticklabels([str(n) for n in N_values], rotation=45)
ax.set_ylim(0, 0.8)
ax.legend(fontsize=7.5, loc="upper left")
ax.grid(True, alpha=0.3)

# ── Panel (b): Per-dataset method comparison ─────────────────────────
ax = axes[1]
x = np.arange(len(datasets))
width = 0.25

bars_ext = ax.bar(x - width, methods["ext_pair_f1"], width,
                  label="Extraction", color="tab:green", alpha=0.85)
bars_gen = ax.bar(x, methods["gen_pair_f1"], width,
                  label="Generation", color="tab:orange", alpha=0.85)
bars_sel = ax.bar(x + width, methods["sel_pair_f1"], width,
                  label="Selection", color="tab:blue", alpha=0.85)

ax.set_ylabel("Pair F1")
ax.set_title("(b) Method comparison by dataset")
ax.set_xticks(x)
ax.set_xticklabels([short_labels[ds] for ds in datasets], rotation=45, ha="right")
ax.set_ylim(0, 0.9)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3, axis="y")

# ── Panel (c): Performance vs cost ──────────────────────────────────
ax = axes[2]

method_summary = {
    "Extraction": {"f1": ext_mean_f1, "cost": ext_cost},
    "Generation": {"f1": gen_mean_f1, "cost": gen_cost},
    "Selection": {"f1": methods["sel_pair_f1"].mean(), "cost": sel_cost},
}

colors_map = {"Extraction": "tab:green", "Generation": "tab:orange", "Selection": "tab:blue"}

for name, vals in method_summary.items():
    ax.scatter(vals["cost"], vals["f1"], s=150, color=colors_map[name],
              label=name, zorder=5, edgecolors="black", linewidth=0.5)
    ax.annotate(name, (vals["cost"], vals["f1"]),
                textcoords="offset points", xytext=(8, -5), fontsize=9)

# Also plot per-dataset points (smaller)
for ds in datasets:
    row = methods[methods["dataset"] == ds].iloc[0]
    # Extraction per-dataset cost
    mf = Path(f"../data/{ds}/evidence_llm/metrics.json")
    if mf.exists():
        m = json.load(open(mf))
        ax.scatter(m["total_cost"], row["ext_pair_f1"], s=30,
                  color="tab:green", alpha=0.4, zorder=3)
    # Generation per-dataset cost
    mf = Path(f"../data/{ds}/evidence_generated/metrics.json")
    if mf.exists():
        m = json.load(open(mf))
        ax.scatter(m["total_cost"], row["gen_pair_f1"], s=30,
                  color="tab:orange", alpha=0.4, zorder=3)
    # Selection per-dataset cost (at best N)
    bn = best_named[best_named["dataset"] == ds].iloc[0]
    best_n = int(bn["N"])
    mf = Path(f"../data/{ds}/evidence_selected/metrics_top{best_n}.json")
    if mf.exists():
        m = json.load(open(mf))
        ax.scatter(m["total_cost"], row["sel_pair_f1"], s=30,
                  color="tab:blue", alpha=0.4, zorder=3)

ax.set_xlabel("Cost (USD, 7 datasets)")
ax.set_ylabel("Mean pair F1")
ax.set_title("(c) Performance vs. cost")
ax.set_ylim(0, 0.8)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

plt.savefig(FIG_DIR / "fig_selection_sweep.pdf", bbox_inches="tight", dpi=150)
plt.savefig(FIG_DIR / "fig_selection_sweep.png", bbox_inches="tight", dpi=150)
print(f"Saved {FIG_DIR / 'fig_selection_sweep.pdf'}")

# Print summary
print(f"\nMethod summary:")
for name, vals in method_summary.items():
    print(f"  {name}: pair F1 = {vals['f1']:.3f}, cost = ${vals['cost']:.2f}")
