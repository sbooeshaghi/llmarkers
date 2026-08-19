import Mathlib

/-!
# Marker identifiability

This file formalizes the combinatorial core of marker-gene identification under
binarization. A marker matrix is a function

  `X : Cell → Gene → Bool`

where `X c g = true` means gene `g` is reported as a marker for cell type or
marker profile `c`.

The main theorem says that if a selected marker panel separates all cell types,
then the number of distinguishable cell types is bounded by the number of binary
codes available from that panel:

  `Fintype.card Cell ≤ 2 ^ S.card`.

This is intentionally independent of any biological assumptions. The biological
work enters when `Cell`, `Gene`, and `X` are instantiated from LLMarkers.
-/

namespace MarkerIdentifiability

open scoped BigOperators

variable {Cell Gene : Type}

/-- A binary marker matrix. -/
abbrev MarkerMatrix (Cell Gene : Type) := Cell → Gene → Bool

/--
The binary signature of a cell type/profile on a selected finite marker panel.
The domain is the subtype of genes contained in `S`, so the signature has exactly
`S.card` binary coordinates.
-/
def signature (X : MarkerMatrix Cell Gene) (S : Finset Gene) (c : Cell) :
    {g // g ∈ S} → Bool :=
  fun g => X c g.1

/--
A marker set separates a collection of cell types/profiles when every distinct
pair differs on at least one selected marker.
-/
def Separates [DecidableEq Gene] (X : MarkerMatrix Cell Gene) (S : Finset Gene) : Prop :=
  ∀ c₁ c₂ : Cell, c₁ ≠ c₂ → ∃ g : Gene, g ∈ S ∧ X c₁ g ≠ X c₂ g

/--
Two cell types/profiles are equivalent at marker panel `S` when they have the
same binary value for every selected marker.
-/
def SameOn [DecidableEq Gene] (X : MarkerMatrix Cell Gene) (S : Finset Gene)
    (c₁ c₂ : Cell) : Prop :=
  ∀ g : Gene, g ∈ S → X c₁ g = X c₂ g

/--
A marker set separates a specified finite collection of cell types/profiles.
This is the finite-set version used for local study-level comparison sets.
-/
def SeparatesOn [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (S : Finset Gene) (Cset : Finset Cell) : Prop :=
  ∀ c₁ : Cell, c₁ ∈ Cset → ∀ c₂ : Cell, c₂ ∈ Cset → c₁ ≠ c₂ →
    ∃ g : Gene, g ∈ S ∧ X c₁ g ≠ X c₂ g

/--
The pairwise difference set for two cell types/profiles over a finite candidate
gene universe. It contains the genes whose binary marker values differ between
the two profiles.
-/
def PairDifferenceSet [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (Genes : Finset Gene) (c₁ c₂ : Cell) : Finset Gene :=
  Genes.filter (fun g => X c₁ g ≠ X c₂ g)

/--
A marker panel hits every pairwise difference set in a comparison set. This is
the hitting-set view of marker-panel selection.
-/
def HitsPairwiseDifferences [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (Genes S : Finset Gene) (Cset : Finset Cell) : Prop :=
  ∀ c₁ : Cell, c₁ ∈ Cset → ∀ c₂ : Cell, c₂ ∈ Cset → c₁ ≠ c₂ →
    ∃ g : Gene, g ∈ S ∧ g ∈ PairDifferenceSet X Genes c₁ c₂

/--
If the selected panel is contained in the candidate gene universe, then
separation is equivalent to hitting every pairwise difference set.
-/
theorem separatesOn_iff_hitsPairwiseDifferences [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {Genes S : Finset Gene} {Cset : Finset Cell}
    (hSGenes : S ⊆ Genes) :
    SeparatesOn X S Cset ↔ HitsPairwiseDifferences X Genes S Cset := by
  constructor
  · intro hsep c₁ hc₁ c₂ hc₂ hne
    rcases hsep c₁ hc₁ c₂ hc₂ hne with ⟨g, hgS, hdiff⟩
    refine ⟨g, hgS, ?_⟩
    simp [PairDifferenceSet, hSGenes hgS, hdiff]
  · intro hhit c₁ hc₁ c₂ hc₂ hne
    rcases hhit c₁ hc₁ c₂ hc₂ hne with ⟨g, hgS, hgDiff⟩
    refine ⟨g, hgS, ?_⟩
    simp [PairDifferenceSet] at hgDiff
    exact hgDiff.2

/--
If two distinct cell types/profiles in a comparison set have the same binary
signature on a marker panel, then that marker panel does not separate the
comparison set.
-/
theorem not_separatesOn_of_sameOn_pair [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} {Cset : Finset Cell}
    {c₁ c₂ : Cell} (hc₁ : c₁ ∈ Cset) (hc₂ : c₂ ∈ Cset) (hne : c₁ ≠ c₂)
    (hsame : SameOn X S c₁ c₂) :
    ¬ SeparatesOn X S Cset := by
  intro hsep
  rcases hsep c₁ hc₁ c₂ hc₂ hne with ⟨g, hgS, hdiff⟩
  exact hdiff (hsame g hgS)

/--
The type-level separation definition is the special case of finite-set
separation over all cells/profiles.
-/
theorem separatesOn_univ_iff_separates [Fintype Cell] [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} :
    SeparatesOn X S Finset.univ ↔ Separates X S := by
  constructor
  · intro h c₁ c₂ hne
    exact h c₁ (by simp) c₂ (by simp) hne
  · intro h c₁ _hc₁ c₂ _hc₂ hne
    exact h c₁ c₂ hne

/--
Global separation restricts to local separation. If a marker panel separates a
larger comparison set, then it separates every smaller comparison set.
-/
theorem separatesOn_subset [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {S : Finset Gene} {Local Global : Finset Cell}
    (hsubset : Local ⊆ Global) (hglobal : SeparatesOn X S Global) :
    SeparatesOn X S Local := by
  intro c₁ hc₁ c₂ hc₂ hne
  exact hglobal c₁ (hsubset hc₁) c₂ (hsubset hc₂) hne

/--
Adding marker genes cannot destroy finite-set separation. If marker panel `S`
separates a comparison set, then every larger marker panel `T` also separates
that same comparison set.
-/
theorem separatesOn_marker_mono [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {S T : Finset Gene} {Cset : Finset Cell}
    (hST : S ⊆ T) (hS : SeparatesOn X S Cset) :
    SeparatesOn X T Cset := by
  intro c₁ hc₁ c₂ hc₂ hne
  rcases hS c₁ hc₁ c₂ hc₂ hne with ⟨g, hgS, hdiff⟩
  exact ⟨g, hST hgS, hdiff⟩

/--
Global separation implies local separation. This is the converse direction that
is valid for marker transfer: a panel that separates an atlas-scale comparison
set also separates every study-level subset of that comparison set.
-/
theorem global_separation_implies_local_separation [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} {Local Global : Finset Cell}
    (hsubset : Local ⊆ Global) (hglobal : SeparatesOn X S Global) :
    SeparatesOn X S Local :=
  separatesOn_subset hsubset hglobal

/--
Marker validity is antitone in the comparison set and monotone in the marker
panel. A panel that separates a larger comparison set still separates any smaller
comparison set, and it remains separating after adding marker genes.
-/
theorem separatesOn_antitone_cells_mono_markers [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S T : Finset Gene} {Local Global : Finset Cell}
    (hLocal : Local ⊆ Global) (hST : S ⊆ T)
    (hglobal : SeparatesOn X S Global) :
    SeparatesOn X T Local :=
  separatesOn_marker_mono hST (separatesOn_subset hLocal hglobal)

/--
For a fixed comparison set, the separating marker panels form an upward-closed
set under marker-panel inclusion.
-/
def SeparatingPanels [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (Cset : Finset Cell) : Set (Finset Gene) :=
  {S | SeparatesOn X S Cset}

/--
For a fixed marker panel, the comparison sets it separates form a downward-closed
set under cell-set inclusion.
-/
def SeparatedComparisonSets [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (S : Finset Gene) : Set (Finset Cell) :=
  {Cset | SeparatesOn X S Cset}

theorem separatingPanels_upward_closed [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {Cset : Finset Cell} {S T : Finset Gene}
    (hS : S ∈ SeparatingPanels X Cset) (hST : S ⊆ T) :
    T ∈ SeparatingPanels X Cset :=
  separatesOn_marker_mono hST hS

theorem separatedComparisonSets_downward_closed [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} {Local Global : Finset Cell}
    (hGlobal : Global ∈ SeparatedComparisonSets X S) (hLocal : Local ⊆ Global) :
    Local ∈ SeparatedComparisonSets X S :=
  separatesOn_subset hLocal hGlobal

/--
A marker set separates one profile from a finite comparison set. Empirically,
this captures whether a local marker claim for one profile lifts to an
outside-paper or atlas-scale comparison set.
-/
def SeparatesFrom [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (S : Finset Gene) (c : Cell) (D : Finset Cell) : Prop :=
  ∀ d : Cell, d ∈ D → c ≠ d → ∃ g : Gene, g ∈ S ∧ X c g ≠ X d g

/--
A collection of experiments covers all pairwise comparisons in a target
comparison set when every distinct pair of target cell types appears together in
at least one experiment.
-/
def PairCovered [DecidableEq Cell] (Experiments : Finset (Finset Cell))
    (Global : Finset Cell) : Prop :=
  ∀ c₁ : Cell, c₁ ∈ Global → ∀ c₂ : Cell, c₂ ∈ Global → c₁ ≠ c₂ →
    ∃ E : Finset Cell, E ∈ Experiments ∧ c₁ ∈ E ∧ c₂ ∈ E

/--
Each experiment contributes at most `q` ordered, distinct comparison pairs inside
the target global family. If an experiment contains at most `r` relevant cell
types, then one can take `q = r * r - r` (the number of ordered off-diagonal
pairs among `r` objects); the theorem below keeps `q` abstract so that users can
also plug in tighter biological or admissibility-specific capacities.
-/
def ExperimentPairCapacityAtMost [DecidableEq Cell]
    (Experiments : Finset (Finset Cell)) (Global : Finset Cell) (q : ℕ) : Prop :=
  ∀ E : Finset Cell, E ∈ Experiments → (E ∩ Global).offDiag.card ≤ q

/--
The ordered comparison pairs observed by a collection of experiments, restricted
to a target global family. Each experiment contributes the ordered off-diagonal
pairs among the global cell types it contains, and the collection contributes
the union of those pairs.
-/
def ObservedPairSet [DecidableEq Cell] (Experiments : Finset (Finset Cell))
    (Global : Finset Cell) : Finset (Cell × Cell) :=
  Experiments.biUnion (fun E : Finset Cell => (E ∩ Global).offDiag)

/--
A collection of experiments covers all required pairwise comparisons in an
admissible comparison graph. The predicate `Admissible c₁ c₂` encodes whether
the pair is required or biologically/experimentally meaningful to compare.
-/
def AdmissiblePairCovered [DecidableEq Cell] (Admissible : Cell → Cell → Prop)
    (Experiments : Finset (Finset Cell)) (Global : Finset Cell) : Prop :=
  ∀ c₁ : Cell, c₁ ∈ Global → ∀ c₂ : Cell, c₂ ∈ Global → c₁ ≠ c₂ →
    Admissible c₁ c₂ →
      ∃ E : Finset Cell, E ∈ Experiments ∧ c₁ ∈ E ∧ c₂ ∈ E

/--
Every experiment in a collection is separated by the same marker panel.
-/
def ExperimentsSeparate [DecidableEq Cell] [DecidableEq Gene]
    (X : MarkerMatrix Cell Gene) (S : Finset Gene)
    (Experiments : Finset (Finset Cell)) : Prop :=
  ∀ E : Finset Cell, E ∈ Experiments → SeparatesOn X S E

/--
Marker separation restricted to admissible comparison pairs.
-/
def SeparatesAdmissibleOn [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (S : Finset Gene) (Global : Finset Cell) (Admissible : Cell → Cell → Prop) : Prop :=
  ∀ c₁ : Cell, c₁ ∈ Global → ∀ c₂ : Cell, c₂ ∈ Global → c₁ ≠ c₂ →
    Admissible c₁ c₂ → ∃ g : Gene, g ∈ S ∧ X c₁ g ≠ X c₂ g

/--
If experiments cover every target pair, and the same marker panel separates each
experiment, then that marker panel separates the global target comparison set.
-/
theorem separatesOn_of_pairCovered_experiments [DecidableEq Cell] [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene}
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell}
    (hcover : PairCovered Experiments Global)
    (hsep : ExperimentsSeparate X S Experiments) :
    SeparatesOn X S Global := by
  intro c₁ hc₁ c₂ hc₂ hne
  rcases hcover c₁ hc₁ c₂ hc₂ hne with ⟨E, hE, hc₁E, hc₂E⟩
  exact hsep E hE c₁ hc₁E c₂ hc₂E hne

/--
If experiments cover every admissible target pair, and the same marker panel
separates each experiment, then that marker panel separates the admissible
comparison graph.
-/
theorem separatesAdmissibleOn_of_pairCovered_experiments
    [DecidableEq Cell] [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} {Admissible : Cell → Cell → Prop}
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell}
    (hcover : AdmissiblePairCovered Admissible Experiments Global)
    (hsep : ExperimentsSeparate X S Experiments) :
    SeparatesAdmissibleOn X S Global Admissible := by
  intro c₁ hc₁ c₂ hc₂ hne hadm
  rcases hcover c₁ hc₁ c₂ hc₂ hne hadm with ⟨E, hE, hc₁E, hc₂E⟩
  exact hsep E hE c₁ hc₁E c₂ hc₂E hne

/--
Ordinary pair coverage is the special case of admissible pair coverage where
every distinct pair is admissible.
-/
theorem pairCovered_iff_admissiblePairCovered_true [DecidableEq Cell]
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell} :
    PairCovered Experiments Global ↔
      AdmissiblePairCovered (fun _ _ => True) Experiments Global := by
  constructor
  · intro hcover c₁ hc₁ c₂ hc₂ hne _hadm
    exact hcover c₁ hc₁ c₂ hc₂ hne
  · intro hcover c₁ hc₁ c₂ hc₂ hne
    exact hcover c₁ hc₁ c₂ hc₂ hne True.intro

/--
The observed pair set after adding one more experiment is the union of the new
experiment's pair set with the previously observed pairs.
-/
theorem observedPairSet_insert [DecidableEq Cell]
    (Experiments : Finset (Finset Cell)) (E Global : Finset Cell) :
    ObservedPairSet (insert E Experiments) Global =
      (E ∩ Global).offDiag ∪ ObservedPairSet Experiments Global := by
  ext pair
  simp [ObservedPairSet]

/--
Adding an experiment increases observed pair coverage by its ordered pair count,
minus the ordered pairs already observed. This is the formal overlap correction:
overlap is useful replication, but it does not add new pairwise comparisons.
-/
theorem observedPairSet_insert_card_eq_add_sub_overlap [DecidableEq Cell]
    (Experiments : Finset (Finset Cell)) (E Global : Finset Cell) :
    (ObservedPairSet (insert E Experiments) Global).card =
      (E ∩ Global).offDiag.card + (ObservedPairSet Experiments Global).card -
        ((E ∩ Global).offDiag ∩ ObservedPairSet Experiments Global).card := by
  rw [observedPairSet_insert, Finset.card_union]

/--
The overlap between the ordered pair sets of two experiments is exactly the
ordered pair set on their shared global cell types.
-/
theorem offDiag_inter_offDiag_eq [DecidableEq Cell] (A B : Finset Cell) :
    A.offDiag ∩ B.offDiag = (A ∩ B).offDiag := by
  ext pair
  simp [Finset.mem_offDiag, and_assoc, and_left_comm, and_comm]

/--
For two experiments, the observed ordered pair count is the sum of their ordered
pair counts minus the ordered pairs duplicated by the cell types they share.
-/
theorem two_experiment_pair_union_card_eq_add_sub_shared [DecidableEq Cell]
    (E₁ E₂ Global : Finset Cell) :
    ((E₁ ∩ Global).offDiag ∪ (E₂ ∩ Global).offDiag).card =
      (E₁ ∩ Global).offDiag.card + (E₂ ∩ Global).offDiag.card -
        (E₁ ∩ E₂ ∩ Global).offDiag.card := by
  rw [Finset.card_union]
  congr 1
  rw [offDiag_inter_offDiag_eq]
  congr 1
  ext c
  simp [and_assoc, and_left_comm, and_comm]

/--
If local experiments cover every ordered distinct pair in a global comparison
family, then every global ordered pair lies in the union of the ordered pairs
observed inside individual experiments.
-/
theorem offDiag_subset_experimentPairUnion_of_pairCovered [DecidableEq Cell]
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell}
    (hcover : PairCovered Experiments Global) :
    Global.offDiag ⊆
      Experiments.biUnion (fun E : Finset Cell => (E ∩ Global).offDiag) := by
  intro pair hpair
  rw [Finset.mem_offDiag] at hpair
  rcases hcover pair.1 hpair.1 pair.2 hpair.2.1 hpair.2.2 with
    ⟨E, hE, hp₁E, hp₂E⟩
  rw [Finset.mem_biUnion]
  refine ⟨E, hE, ?_⟩
  rw [Finset.mem_offDiag]
  exact ⟨by simp [hp₁E, hpair.1], by simp [hp₂E, hpair.2.1], hpair.2.2⟩

/--
Pair coverage imposes a counting lower bound. The number of ordered distinct
global pairs is at most the total number of ordered distinct pairs supplied by
the local experiments.
-/
theorem pairCovered_offDiag_card_le_sum_experiment_offDiag [DecidableEq Cell]
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell}
    (hcover : PairCovered Experiments Global) :
    Global.offDiag.card ≤
      ∑ E ∈ Experiments, ((E ∩ Global).offDiag.card) := by
  exact (Finset.card_le_card
    (offDiag_subset_experimentPairUnion_of_pairCovered hcover)).trans
      Finset.card_biUnion_le

/--
If every local experiment contributes at most `q` ordered distinct comparison
pairs inside the target global family, then covering the global family requires
enough experiments to cover all ordered distinct global pairs.

Since `Global.offDiag.card = Global.card * Global.card - Global.card`, this is
the ordered-pair version of the usual
`choose(k,2) / choose(r,2)` coverage lower bound.
-/
theorem pairCovered_offDiag_card_le_experiments_mul_pairCapacity [DecidableEq Cell]
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell} {q : ℕ}
    (hcover : PairCovered Experiments Global)
    (hcap : ExperimentPairCapacityAtMost Experiments Global q) :
    Global.offDiag.card ≤ Experiments.card * q := by
  exact (Finset.card_le_card
    (offDiag_subset_experimentPairUnion_of_pairCovered hcover)).trans
      (Finset.card_biUnion_le_card_mul Experiments
        (fun E : Finset Cell => (E ∩ Global).offDiag) q hcap)

/--
The same lower bound written only in terms of the number of global cell types
`Global.card`, the number of local experiments `Experiments.card`, and the
per-experiment ordered-pair capacity `q`.
-/
theorem pairCovered_global_orderedPair_count_le_experiments_mul_pairCapacity
    [DecidableEq Cell]
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell} {q : ℕ}
    (hcover : PairCovered Experiments Global)
    (hcap : ExperimentPairCapacityAtMost Experiments Global q) :
    Global.card * Global.card - Global.card ≤ Experiments.card * q := by
  simpa [Finset.offDiag_card] using
    pairCovered_offDiag_card_le_experiments_mul_pairCapacity
      (Experiments := Experiments) (Global := Global) (q := q) hcover hcap

/--
The experiment lower bound with explicit symbols:
if `k` global cell types are to be covered by `m` experiments, each contributing
at most `q` ordered distinct relevant pairs, then `k * k - k ≤ m * q`.
-/
theorem pairCovered_global_orderedPair_count_le_of_card_eq [DecidableEq Cell]
    {Experiments : Finset (Finset Cell)} {Global : Finset Cell} {k m q : ℕ}
    (hcover : PairCovered Experiments Global)
    (hcap : ExperimentPairCapacityAtMost Experiments Global q)
    (hk : Global.card = k) (hm : Experiments.card = m) :
    k * k - k ≤ m * q := by
  simpa [hk, hm] using
    pairCovered_global_orderedPair_count_le_experiments_mul_pairCapacity
      (Experiments := Experiments) (Global := Global) (q := q) hcover hcap

/--
An ideal one-vs-all marker panel separates every target cell type from every
individual cell type in its complement. This is stronger than a lossy
one-vs-rest differential-expression test against an aggregated complement.
-/
def OneVsAllSeparates [DecidableEq Cell] [DecidableEq Gene]
    (X : MarkerMatrix Cell Gene) (S : Finset Gene) (Global : Finset Cell) : Prop :=
  ∀ c : Cell, c ∈ Global → SeparatesFrom X S c (Global.erase c)

/--
At the binary marker-signature level, ideal one-vs-all separation is equivalent
to pairwise global separation.
-/
theorem oneVsAllSeparates_iff_separatesOn [DecidableEq Cell] [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} {Global : Finset Cell} :
    OneVsAllSeparates X S Global ↔ SeparatesOn X S Global := by
  constructor
  · intro hone c₁ hc₁ c₂ hc₂ hne
    have hc₂erase : c₂ ∈ Global.erase c₁ := by
      simp [Finset.mem_erase, hne.symm, hc₂]
    exact hone c₁ hc₁ c₂ hc₂erase hne
  · intro hsep c hc d hd hne
    have hdGlobal : d ∈ Global := (Finset.mem_erase.mp hd).2
    exact hsep c hc d hdGlobal hne

/--
If a panel separates a global comparison set, then every profile in that set is
separated from every specified subset of that global set.
-/
theorem global_separation_gives_lift [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {S : Finset Gene} {Global D : Finset Cell} {c : Cell}
    (hc : c ∈ Global) (hD : D ⊆ Global) (hglobal : SeparatesOn X S Global) :
    SeparatesFrom X S c D := by
  intro d hd hne
  exact hglobal c hc d (hD hd) hne

/-!
## Local contrasts and comparison backgrounds

The binary marker matrix above is the projection most reported marker tables
store. The contrast-level object is richer: a study, a local partition, a target
group, a comparison group or background, and a gene.

At this level, one-vs-rest is not a primitive global marker. It is a weighted
background contrast, and when the weights sum to one it decomposes exactly into
a weighted sum of pairwise target-vs-comparison contrasts.
-/

/-- Mean or pseudobulk expression profile for each local group in a partition. -/
abbrev LocalMeanProfile (Study Partition Group Gene : Type) :=
  Study → Partition → Group → Gene → ℝ

/--
The pairwise contrast for one gene between a target local group and one
comparison group inside a specified study partition.
-/
def LocalPairwiseContrast {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene)
    (study : Study) (partition : Partition)
    (target comparison : Group) (gene : Gene) : ℝ :=
  μ study partition target gene - μ study partition comparison gene

/--
A one-vs-background contrast for one gene. The background is a finite set of
comparison groups with weights, typically the other groups in the local
partition.
-/
def LocalBackgroundContrast {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene)
    (study : Study) (partition : Partition) (target : Group)
    (background : Finset Group) (w : Group → ℝ) (gene : Gene) : ℝ :=
  μ study partition target gene -
    (∑ h ∈ background, w h * μ study partition h gene)

/--
If the background weights sum to one, a one-vs-background contrast is exactly a
weighted sum of the pairwise contrasts from the target group to each background
group. This is the formal version of the claim that one-vs-rest markers are
background-dependent mixtures of pairwise local contrasts.
-/
theorem localBackgroundContrast_eq_weighted_pairwise
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene}
    {study : Study} {partition : Partition} {target : Group}
    {background : Finset Group} {w : Group → ℝ} {gene : Gene}
    (hweights : (∑ h ∈ background, w h) = 1) :
    LocalBackgroundContrast μ study partition target background w gene =
      (∑ h ∈ background,
        w h * LocalPairwiseContrast μ study partition target h gene) := by
  calc
    LocalBackgroundContrast μ study partition target background w gene
        = (∑ h ∈ background, w h) * μ study partition target gene -
            (∑ h ∈ background, w h * μ study partition h gene) := by
          simp [LocalBackgroundContrast, hweights]
    _ = (∑ h ∈ background, w h * μ study partition target gene) -
            (∑ h ∈ background, w h * μ study partition h gene) := by
          rw [Finset.sum_mul]
    _ = ∑ h ∈ background,
            (w h * μ study partition target gene -
              w h * μ study partition h gene) := by
          rw [← Finset.sum_sub_distrib]
    _ = ∑ h ∈ background,
            w h * LocalPairwiseContrast μ study partition target h gene := by
          apply Finset.sum_congr rfl
          intro h _hh
          rw [LocalPairwiseContrast]
          ring

/-- A gene is a pairwise marker when its contrast exceeds a chosen threshold. -/
def PairwiseContrastMarker {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition)
    (target comparison : Group) (gene : Gene) : Prop :=
  threshold < LocalPairwiseContrast μ study partition target comparison gene

/--
A gene is a marker against a weighted background when the one-vs-background
contrast exceeds a chosen threshold.
-/
def BackgroundContrastMarker {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (background : Finset Group) (w : Group → ℝ) (gene : Gene) : Prop :=
  threshold < LocalBackgroundContrast μ study partition target background w gene

/--
A gene is a marker for a target group relative to a specified finite comparison
family when it passes the contrast threshold against every admissible comparison
group in that family.
-/
def ContrastFamilyMarker {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) (gene : Gene) : Prop :=
  ∀ comparison : Group, comparison ∈ comparisons →
    PairwiseContrastMarker μ threshold study partition target comparison gene

/--
The pairwise marker-gene set for a fixed target-vs-comparison contrast.
-/
def PairwiseMarkerGenes {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target comparison : Group) :
    Set Gene :=
  {gene | PairwiseContrastMarker μ threshold study partition target comparison gene}

/--
The marker-gene set for a target relative to a finite comparison family.
-/
def ContrastFamilyMarkerGenes {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) : Set Gene :=
  {gene | ContrastFamilyMarker μ threshold study partition target comparisons gene}

/--
An abstract marker-family rule assigns a marker-gene set to each finite
comparison family after the pairwise marker sets have been fixed.

The axioms say that the empty family is mathematically neutral, singleton
families agree with the pairwise marker sets, and marker status for a union of
comparison families is conjunctive: the gene must satisfy both component marker
claims.
-/
structure MarkerFamilyAxioms {Group Gene : Type} [DecidableEq Group]
    (pairwise : Group → Set Gene) (family : Finset Group → Set Gene) : Prop where
  empty_neutral : family ∅ = Set.univ
  singleton_agreement : ∀ comparison : Group, family {comparison} = pairwise comparison
  union_conjunctive :
    ∀ C D : Finset Group, family (C ∪ D) = family C ∩ family D

/--
Any marker-family rule satisfying the axioms marks a gene for a comparison
family exactly when the gene belongs to every pairwise marker set indexed by
that family.
-/
theorem markerFamilyAxioms_mem_iff_all_pairwise
    {Group Gene : Type} [DecidableEq Group]
    {pairwise : Group → Set Gene} {family : Finset Group → Set Gene}
    (haxioms : MarkerFamilyAxioms pairwise family)
    (comparisons : Finset Group) (gene : Gene) :
    gene ∈ family comparisons ↔
      ∀ comparison : Group, comparison ∈ comparisons → gene ∈ pairwise comparison := by
  refine Finset.induction_on comparisons ?empty ?insert
  · rw [haxioms.empty_neutral]
    simp
  · intro comparison comparisons hnotMem ih
    have hinsert :
        (insert comparison comparisons : Finset Group) =
          ({comparison} : Finset Group) ∪ comparisons := by
      ext h
      simp [Finset.mem_insert]
    rw [hinsert, haxioms.union_conjunctive, haxioms.singleton_agreement]
    simp [ih]

/--
The axioms force the intersection representation: a marker-family rule is the
intersection of its pairwise marker sets over the specified comparison family.
-/
theorem markerFamilyAxioms_eq_iInter_pairwise
    {Group Gene : Type} [DecidableEq Group]
    {pairwise : Group → Set Gene} {family : Finset Group → Set Gene}
    (haxioms : MarkerFamilyAxioms pairwise family)
    (comparisons : Finset Group) :
    family comparisons =
      ⋂ comparison : {h // h ∈ comparisons}, pairwise comparison.1 := by
  ext gene
  rw [markerFamilyAxioms_mem_iff_all_pairwise haxioms]
  simp

/--
The marker-family rule satisfying the axioms for a fixed collection of pairwise
marker sets is unique.
-/
theorem markerFamilyAxioms_unique
    {Group Gene : Type} [DecidableEq Group]
    {pairwise : Group → Set Gene} {family₁ family₂ : Finset Group → Set Gene}
    (hfamily₁ : MarkerFamilyAxioms pairwise family₁)
    (hfamily₂ : MarkerFamilyAxioms pairwise family₂) :
    family₁ = family₂ := by
  funext comparisons
  rw [markerFamilyAxioms_eq_iInter_pairwise hfamily₁,
    markerFamilyAxioms_eq_iInter_pairwise hfamily₂]

/--
The concrete comparison-family marker-gene definition used below satisfies the
abstract marker-family axioms.
-/
theorem contrastFamilyMarkerGenes_satisfies_markerFamilyAxioms
    {Study Partition Group Gene : Type} [DecidableEq Group]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group} :
    MarkerFamilyAxioms
      (fun comparison : Group =>
        PairwiseMarkerGenes μ threshold study partition target comparison)
      (fun comparisons : Finset Group =>
        ContrastFamilyMarkerGenes μ threshold study partition target comparisons) := by
  refine ⟨?empty, ?singleton, ?union⟩
  · ext gene
    simp [ContrastFamilyMarkerGenes, ContrastFamilyMarker]
  · intro comparison
    ext gene
    simp [ContrastFamilyMarkerGenes, ContrastFamilyMarker, PairwiseMarkerGenes]
  · intro C D
    ext gene
    simp only [ContrastFamilyMarkerGenes, ContrastFamilyMarker, Set.mem_setOf_eq,
      Set.mem_inter_iff,
      Finset.mem_union]
    constructor
    · intro hmarker
      constructor
      · intro comparison hcomparison
        exact hmarker comparison (Or.inl hcomparison)
      · intro comparison hcomparison
        exact hmarker comparison (Or.inr hcomparison)
    · intro hmarker comparison hcomparison
      rcases hcomparison with hcomparison | hcomparison
      · exact hmarker.1 comparison hcomparison
      · exact hmarker.2 comparison hcomparison

/--
A gene belongs to the comparison-family marker set exactly when it belongs to
every pairwise marker set for comparisons in that family.
-/
theorem mem_contrastFamilyMarkerGenes_iff_mem_all_pairwiseMarkerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {gene : Gene} :
    gene ∈ ContrastFamilyMarkerGenes μ threshold study partition target comparisons ↔
      ∀ comparison : Group, comparison ∈ comparisons →
        gene ∈ PairwiseMarkerGenes μ threshold study partition target comparison := by
  rfl

/--
The comparison-family marker set is the intersection of the pairwise marker sets
over the specified comparison family. This is the formal statement behind
reporting pairwise markers for every partition: later aggregate analyses can
reconstruct marker sets for any desired local comparison family by intersection.
-/
theorem contrastFamilyMarkerGenes_eq_iInter_pairwiseMarkerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} :
    ContrastFamilyMarkerGenes μ threshold study partition target comparisons =
      ⋂ comparison : {h // h ∈ comparisons},
        PairwiseMarkerGenes μ threshold study partition target comparison.1 := by
  ext gene
  simp [ContrastFamilyMarkerGenes, PairwiseMarkerGenes, ContrastFamilyMarker]

/--
An abstract marker panel is a hitting set for pairwise marker sets. The panel
need not contain a gene that works against every comparison; instead, each
comparison must be covered by at least one selected gene.
-/
def HitsPairwiseMarkerSets {Group Gene : Type}
    (pairwise : Group → Set Gene) (comparisons : Finset Group)
    (panel : Finset Gene) : Prop :=
  ∀ comparison : Group, comparison ∈ comparisons →
    ∃ gene : Gene, gene ∈ panel ∧ gene ∈ pairwise comparison

/--
An abstract marker-panel rule assigns a validity predicate to each finite
comparison family and selected gene panel after pairwise marker sets have been
fixed.

The axioms say that the empty comparison family is neutral, a singleton
comparison family is covered exactly when the panel intersects that pairwise
marker set, and coverage of a union of comparison families is conjunctive.
-/
structure MarkerPanelAxioms {Group Gene : Type} [DecidableEq Group]
    (pairwise : Group → Set Gene)
    (panelRule : Finset Group → Finset Gene → Prop) : Prop where
  empty_neutral : ∀ panel : Finset Gene, panelRule ∅ panel
  singleton_agreement :
    ∀ comparison : Group, ∀ panel : Finset Gene,
      panelRule {comparison} panel ↔
        ∃ gene : Gene, gene ∈ panel ∧ gene ∈ pairwise comparison
  union_conjunctive :
    ∀ C D : Finset Group, ∀ panel : Finset Gene,
      panelRule (C ∪ D) panel ↔ panelRule C panel ∧ panelRule D panel

/--
The marker-panel axioms force the hitting-set representation: a panel is valid
for a comparison family exactly when it hits every pairwise marker set indexed
by that family.
-/
theorem markerPanelAxioms_iff_hitsPairwiseMarkerSets
    {Group Gene : Type} [DecidableEq Group]
    {pairwise : Group → Set Gene}
    {panelRule : Finset Group → Finset Gene → Prop}
    (haxioms : MarkerPanelAxioms pairwise panelRule)
    (comparisons : Finset Group) (panel : Finset Gene) :
    panelRule comparisons panel ↔
      HitsPairwiseMarkerSets pairwise comparisons panel := by
  refine Finset.induction_on comparisons ?empty ?insert
  · constructor
    · intro _hpanel comparison hcomparison
      simp at hcomparison
    · intro _hhits
      exact haxioms.empty_neutral panel
  · intro comparison comparisons hnotMem ih
    have hinsert :
        (insert comparison comparisons : Finset Group) =
          ({comparison} : Finset Group) ∪ comparisons := by
      ext h
      simp [Finset.mem_insert]
    rw [hinsert, haxioms.union_conjunctive, haxioms.singleton_agreement, ih]
    constructor
    · intro hcovered candidate hcandidate
      rcases hcovered with ⟨hsingleton, hrest⟩
      rcases Finset.mem_insert.mp hcandidate with rfl | hcandidate
      · exact hsingleton
      · exact hrest candidate hcandidate
    · intro hhits
      constructor
      · exact hhits comparison (by simp)
      · intro candidate hcandidate
        exact hhits candidate (by simp [hcandidate])

/--
The hitting-set marker-panel rule satisfies the abstract marker-panel axioms.
-/
theorem hitsPairwiseMarkerSets_satisfies_markerPanelAxioms
    {Group Gene : Type} [DecidableEq Group]
    {pairwise : Group → Set Gene} :
    MarkerPanelAxioms pairwise
      (fun comparisons : Finset Group => HitsPairwiseMarkerSets pairwise comparisons) := by
  refine ⟨?empty, ?singleton, ?union⟩
  · intro panel comparison hcomparison
    simp at hcomparison
  · intro comparison panel
    constructor
    · intro hpanel
      exact hpanel comparison (by simp)
    · intro hhit candidate hcandidate
      have hcandidate_eq : candidate = comparison := by
        simpa using hcandidate
      subst candidate
      exact hhit
  · intro C D panel
    constructor
    · intro hpanel
      constructor
      · intro comparison hcomparison
        exact hpanel comparison (by simp [hcomparison])
      · intro comparison hcomparison
        exact hpanel comparison (by simp [hcomparison])
    · intro hpanel comparison hcomparison
      rcases Finset.mem_union.mp hcomparison with hcomparison | hcomparison
      · exact hpanel.1 comparison hcomparison
      · exact hpanel.2 comparison hcomparison

/--
For fixed pairwise marker sets, any marker-panel rule satisfying the axioms is
unique.
-/
theorem markerPanelAxioms_unique
    {Group Gene : Type} [DecidableEq Group]
    {pairwise : Group → Set Gene}
    {panelRule₁ panelRule₂ : Finset Group → Finset Gene → Prop}
    (hpanelRule₁ : MarkerPanelAxioms pairwise panelRule₁)
    (hpanelRule₂ : MarkerPanelAxioms pairwise panelRule₂) :
    panelRule₁ = panelRule₂ := by
  funext comparisons panel
  apply propext
  rw [markerPanelAxioms_iff_hitsPairwiseMarkerSets hpanelRule₁,
    markerPanelAxioms_iff_hitsPairwiseMarkerSets hpanelRule₂]

/--
A target-specific marker panel covers a comparison family when every comparison
group has at least one selected gene that is a pairwise marker for the target
against that comparison group.
-/
def ContrastFamilyMarkerPanel {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) (panel : Finset Gene) : Prop :=
  ∀ comparison : Group, comparison ∈ comparisons →
    ∃ gene : Gene, gene ∈ panel ∧
      PairwiseContrastMarker μ threshold study partition target comparison gene

/--
The concrete target-specific marker panel definition is exactly the hitting-set
condition over the corresponding pairwise marker-gene sets.
-/
theorem contrastFamilyMarkerPanel_iff_hitsPairwiseMarkerSets
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {panel : Finset Gene} :
    ContrastFamilyMarkerPanel μ threshold study partition target comparisons panel ↔
      HitsPairwiseMarkerSets
        (fun comparison : Group =>
          PairwiseMarkerGenes μ threshold study partition target comparison)
        comparisons panel := by
  constructor
  · intro hpanel comparison hcomparison
    rcases hpanel comparison hcomparison with ⟨gene, hgene_panel, hgene_marker⟩
    exact ⟨gene, hgene_panel, hgene_marker⟩
  · intro hhits comparison hcomparison
    rcases hhits comparison hcomparison with ⟨gene, hgene_panel, hgene_marker⟩
    exact ⟨gene, hgene_panel, hgene_marker⟩

/--
The concrete target-specific marker-panel definition satisfies the abstract
marker-panel axioms.
-/
theorem contrastFamilyMarkerPanel_satisfies_markerPanelAxioms
    {Study Partition Group Gene : Type} [DecidableEq Group]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group} :
    MarkerPanelAxioms
      (fun comparison : Group =>
        PairwiseMarkerGenes μ threshold study partition target comparison)
      (fun comparisons : Finset Group =>
        ContrastFamilyMarkerPanel μ threshold study partition target comparisons) := by
  refine ⟨?empty, ?singleton, ?union⟩
  · intro panel comparison hcomparison
    simp at hcomparison
  · intro comparison panel
    rw [contrastFamilyMarkerPanel_iff_hitsPairwiseMarkerSets]
    exact (hitsPairwiseMarkerSets_satisfies_markerPanelAxioms).singleton_agreement comparison panel
  · intro C D panel
    repeat rw [contrastFamilyMarkerPanel_iff_hitsPairwiseMarkerSets]
    exact (hitsPairwiseMarkerSets_satisfies_markerPanelAxioms).union_conjunctive C D panel

/--
The empty comparison family is covered by every marker panel. Biologically this
is a degenerate case: no alternatives have been specified.
-/
theorem contrastFamilyMarkerPanel_empty_comparisons
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {panel : Finset Gene} :
    ContrastFamilyMarkerPanel μ threshold study partition target ∅ panel := by
  intro comparison hcomparison
  simp at hcomparison

/--
An empty marker panel cannot cover a nonempty comparison family.
-/
theorem not_contrastFamilyMarkerPanel_empty_panel_of_nonempty_comparisons
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group}
    (hcomparisons : comparisons.Nonempty) :
    ¬ ContrastFamilyMarkerPanel μ threshold study partition target comparisons
      (∅ : Finset Gene) := by
  intro hpanel
  rcases hcomparisons with ⟨comparison, hcomparison⟩
  rcases hpanel comparison hcomparison with ⟨gene, hgene_panel, _hgene_marker⟩
  simp at hgene_panel

/--
Adding genes to a covering marker panel preserves coverage.
-/
theorem contrastFamilyMarkerPanel_mono_genes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {panel largerPanel : Finset Gene}
    (hsubset : panel ⊆ largerPanel)
    (hpanel :
      ContrastFamilyMarkerPanel μ threshold study partition target comparisons panel) :
    ContrastFamilyMarkerPanel μ threshold study partition target comparisons largerPanel := by
  intro comparison hcomparison
  rcases hpanel comparison hcomparison with ⟨gene, hgene_panel, hgene_marker⟩
  exact ⟨gene, hsubset hgene_panel, hgene_marker⟩

/--
Restricting the comparison family preserves panel coverage.
-/
theorem contrastFamilyMarkerPanel_subset_comparisons
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {Local Global : Finset Group} {panel : Finset Gene}
    (hsubset : Local ⊆ Global)
    (hglobal :
      ContrastFamilyMarkerPanel μ threshold study partition target Global panel) :
    ContrastFamilyMarkerPanel μ threshold study partition target Local panel := by
  intro comparison hlocal
  exact hglobal comparison (hsubset hlocal)

/--
Marker panels are monotone in selected genes and antitone in comparison scope:
a larger panel that covers a broader comparison family also covers every
restricted comparison family.
-/
theorem contrastFamilyMarkerPanel_antitone_comparisons_mono_genes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {Local Global : Finset Group} {panel largerPanel : Finset Gene}
    (hLocal : Local ⊆ Global) (hPanel : panel ⊆ largerPanel)
    (hglobal :
      ContrastFamilyMarkerPanel μ threshold study partition target Global panel) :
    ContrastFamilyMarkerPanel μ threshold study partition target Local largerPanel :=
  contrastFamilyMarkerPanel_mono_genes hPanel
    (contrastFamilyMarkerPanel_subset_comparisons hLocal hglobal)

/-!
## Comparison difficulty

The marker definitions above treat a comparison family as a finite set of
constraints. That is the right logical object: adding comparisons can only add
constraints, and restricting comparisons can only remove constraints.

Empirically, however, two comparison families with the same or even smaller
cardinality need not be equally easy. A smaller family can contain only close
biological neighbors, while a larger family can contain mostly distant groups.
The following definitions add an optional difficulty layer without changing the
marker definition itself.
-/

/--
A comparison-difficulty score assigns a nonnegative burden to asking whether a
target group can be distinguished from a comparison group. Larger values can be
used for biologically closer or otherwise harder comparisons.
-/
abbrev ComparisonDifficulty (Group : Type) := Group → Group → ℝ

/--
The total difficulty burden of a target's comparison family.
-/
def ComparisonFamilyBurden {Group : Type}
    (difficulty : ComparisonDifficulty Group) (target : Group)
    (comparisons : Finset Group) : ℝ :=
  comparisons.sum (fun comparison => difficulty target comparison)

/--
The empty comparison family has no comparison burden.
-/
theorem comparisonFamilyBurden_empty {Group : Type}
    (difficulty : ComparisonDifficulty Group) (target : Group) :
    ComparisonFamilyBurden difficulty target ∅ = 0 := by
  simp [ComparisonFamilyBurden]

/--
Adding one comparison adds exactly that comparison's difficulty burden.
-/
theorem comparisonFamilyBurden_insert {Group : Type} [DecidableEq Group]
    {difficulty : ComparisonDifficulty Group} {target comparison : Group}
    {comparisons : Finset Group}
    (hnotMem : comparison ∉ comparisons) :
    ComparisonFamilyBurden difficulty target (insert comparison comparisons) =
      difficulty target comparison + ComparisonFamilyBurden difficulty target comparisons := by
  simp [ComparisonFamilyBurden, hnotMem]

/--
For nonnegative difficulty scores, enlarging a comparison family cannot decrease
the total comparison burden.
-/
theorem comparisonFamilyBurden_mono {Group : Type}
    {difficulty : ComparisonDifficulty Group} {target : Group}
    {Local Global : Finset Group}
    (hsubset : Local ⊆ Global)
    (hnonneg : ∀ comparison : Group, comparison ∈ Global →
      0 ≤ difficulty target comparison) :
    ComparisonFamilyBurden difficulty target Local ≤
      ComparisonFamilyBurden difficulty target Global := by
  exact Finset.sum_le_sum_of_subset_of_nonneg hsubset
    (by
      intro comparison hglobal _hnotLocal
      exact hnonneg comparison hglobal)

/--
The high-similarity or high-difficulty part of a comparison family. This can be
used to model close-neighbor contrasts such as immune-cell comparisons inside a
pre-sorted immune dataset.
-/
noncomputable def HardComparisonFamily {Group : Type}
    (similarity : Group → Group → ℝ) (target : Group) (cutoff : ℝ)
    (comparisons : Finset Group) : Finset Group :=
  comparisons.filter (fun comparison => cutoff ≤ similarity target comparison)

/--
The hard-comparison family is a subset of the original comparison family.
-/
theorem hardComparisonFamily_subset {Group : Type}
    {similarity : Group → Group → ℝ} {target : Group} {cutoff : ℝ}
    {comparisons : Finset Group} :
    HardComparisonFamily similarity target cutoff comparisons ⊆ comparisons := by
  intro comparison hcomparison
  exact (Finset.mem_filter.mp hcomparison).1

/--
A panel that covers the full comparison family also covers any hard-neighbor
subfamily induced by a similarity threshold.
-/
theorem contrastFamilyMarkerPanel_hardComparisonFamily
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold cutoff : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {panel : Finset Gene}
    {similarity : Group → Group → ℝ}
    (hpanel :
      ContrastFamilyMarkerPanel μ threshold study partition target comparisons panel) :
    ContrastFamilyMarkerPanel μ threshold study partition target
      (HardComparisonFamily similarity target cutoff comparisons) panel :=
  contrastFamilyMarkerPanel_subset_comparisons hardComparisonFamily_subset hpanel

namespace ComparisonDifficultyExample

/--
A toy comparison universe: one target, one close neighbor, and two distant
neighbors.
-/
inductive Group where
  | target
  | close
  | distant₁
  | distant₂
  deriving DecidableEq

open Group

def smallCloseFamily : Finset Group := {close}

def largerDistantFamily : Finset Group := {distant₁, distant₂}

def difficulty : ComparisonDifficulty Group
  | target, close => 10
  | target, distant₁ => 1
  | target, distant₂ => 1
  | _, _ => 0

/--
The close-neighbor family has fewer comparisons than the distant-neighbor
family.
-/
theorem smallCloseFamily_has_fewer_comparisons :
    smallCloseFamily.card < largerDistantFamily.card := by
  native_decide

/--
The close-neighbor family nevertheless has higher total difficulty burden. This
formalizes the Hildreth-style point: narrowing the comparison family can remove
easy distant comparisons while retaining harder nearby comparisons.
-/
theorem smallCloseFamily_has_larger_burden :
    ComparisonFamilyBurden difficulty target largerDistantFamily <
      ComparisonFamilyBurden difficulty target smallCloseFamily := by
  simp [ComparisonFamilyBurden, smallCloseFamily, largerDistantFamily, difficulty]
  norm_num

end ComparisonDifficultyExample

/--
A singleton marker panel covers a comparison family exactly when its one gene is
a strict comparison-family marker for that family.
-/
theorem singleton_contrastFamilyMarkerPanel_iff_contrastFamilyMarker
    {Study Partition Group Gene : Type} [DecidableEq Gene]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {gene : Gene} :
    ContrastFamilyMarkerPanel μ threshold study partition target comparisons
      ({gene} : Finset Gene) ↔
      ContrastFamilyMarker μ threshold study partition target comparisons gene := by
  constructor
  · intro hpanel comparison hcomparison
    rcases hpanel comparison hcomparison with ⟨gene', hgene'_panel, hgene'_marker⟩
    have hgene' : gene' = gene := by
      simpa using hgene'_panel
    subst gene'
    exact hgene'_marker
  · intro hmarker comparison hcomparison
    exact ⟨gene, by simp, hmarker comparison hcomparison⟩

/--
Any selected strict comparison-family marker is enough to make a panel cover
the comparison family.
-/
theorem contrastFamilyMarkerPanel_of_mem_contrastFamilyMarkerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {panel : Finset Gene} {gene : Gene}
    (hgene_panel : gene ∈ panel)
    (hgene_marker :
      gene ∈ ContrastFamilyMarkerGenes μ threshold study partition target comparisons) :
    ContrastFamilyMarkerPanel μ threshold study partition target comparisons panel := by
  intro comparison hcomparison
  exact ⟨gene, hgene_panel, hgene_marker comparison hcomparison⟩

/--
Every nonempty panel whose genes are all strict comparison-family markers covers
the comparison family.
-/
theorem contrastFamilyMarkerPanel_of_nonempty_subset_contrastFamilyMarkerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {panel : Finset Gene}
    (hpanel_nonempty : panel.Nonempty)
    (hpanel_subset :
      ∀ gene : Gene, gene ∈ panel →
        gene ∈ ContrastFamilyMarkerGenes μ threshold study partition target comparisons) :
    ContrastFamilyMarkerPanel μ threshold study partition target comparisons panel := by
  rcases hpanel_nonempty with ⟨gene, hgene_panel⟩
  exact contrastFamilyMarkerPanel_of_mem_contrastFamilyMarkerGenes hgene_panel
    (hpanel_subset gene hgene_panel)

/--
A minimum target-specific marker panel is a covering panel with minimum
cardinality among all covering panels for the same target and comparison family.
-/
def IsMinimumContrastFamilyMarkerPanel {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) (panel : Finset Gene) : Prop :=
  ContrastFamilyMarkerPanel μ threshold study partition target comparisons panel ∧
    ∀ otherPanel : Finset Gene,
      ContrastFamilyMarkerPanel μ threshold study partition target comparisons otherPanel →
        panel.card ≤ otherPanel.card

/--
An essential panel gene is present in every minimum marker panel for a target
and comparison family.
-/
def EssentialPanelGene {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) (gene : Gene) : Prop :=
  ∀ panel : Finset Gene,
    IsMinimumContrastFamilyMarkerPanel μ threshold study partition target comparisons panel →
      gene ∈ panel

/--
An exchangeable panel gene is present in at least one, but not every, minimum
marker panel for a target and comparison family.
-/
def ExchangeablePanelGene {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) (gene : Gene) : Prop :=
  (∃ panel : Finset Gene,
    IsMinimumContrastFamilyMarkerPanel μ threshold study partition target comparisons panel ∧
      gene ∈ panel) ∧
    ¬ EssentialPanelGene μ threshold study partition target comparisons gene

/--
A redundant panel gene is absent from every minimum marker panel for a target
and comparison family.
-/
def RedundantForMinimumMarkerPanel {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) (gene : Gene) : Prop :=
  ∀ panel : Finset Gene,
    IsMinimumContrastFamilyMarkerPanel μ threshold study partition target comparisons panel →
      gene ∉ panel

/--
An exchangeable panel gene is not essential by definition.
-/
theorem exchangeablePanelGene_not_essential
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {gene : Gene}
    (h : ExchangeablePanelGene μ threshold study partition target comparisons gene) :
    ¬ EssentialPanelGene μ threshold study partition target comparisons gene :=
  h.2

/--
An exchangeable panel gene is witnessed by at least one minimum marker panel
that contains it.
-/
theorem exchangeablePanelGene_mem_some_minimum
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {gene : Gene}
    (h : ExchangeablePanelGene μ threshold study partition target comparisons gene) :
    ∃ panel : Finset Gene,
      IsMinimumContrastFamilyMarkerPanel μ threshold study partition target comparisons panel ∧
        gene ∈ panel :=
  h.1

/-!
Panel performance with positive and negative contexts

The target-specific marker-panel definition above is a validity condition: every
intended comparison is covered by at least one gene in the selected panel. For
practical marker design, one also wants to quantify the tradeoff incurred by
adding genes. The following definitions separate target sensitivity from
off-target hits.
-/

/--
A panel hits a context when at least one selected gene belongs to that context's
marker set.
-/
def PanelHits {Context Gene : Type}
    (markerSets : Context → Set Gene) (panel : Finset Gene)
    (context : Context) : Prop :=
  ∃ gene : Gene, gene ∈ panel ∧ gene ∈ markerSets context

/--
The contexts hit by a marker panel.
-/
noncomputable def CoveredContexts {Context Gene : Type} [DecidableEq Context]
    (markerSets : Context → Set Gene) (contexts : Finset Context)
    (panel : Finset Gene) : Finset Context := by
  classical
  exact contexts.filter (fun context => PanelHits markerSets panel context)

/--
The contexts avoided by a marker panel.
-/
noncomputable def AvoidedContexts {Context Gene : Type} [DecidableEq Context]
    (markerSets : Context → Set Gene) (contexts : Finset Context)
    (panel : Finset Gene) : Finset Context := by
  classical
  exact contexts.filter (fun context => ¬ PanelHits markerSets panel context)

/--
Target coverage count. Dividing by the number of positive contexts gives
sensitivity.
-/
noncomputable def PanelCoverageCount {Context Gene : Type} [DecidableEq Context]
    (markerSets : Context → Set Gene) (contexts : Finset Context)
    (panel : Finset Gene) : Nat :=
  (CoveredContexts markerSets contexts panel).card

/--
Off-target hit count. Dividing by the number of negative contexts gives the
off-target hit rate, and one minus that rate gives specificity.
-/
noncomputable def PanelOffTargetHitCount {Context Gene : Type} [DecidableEq Context]
    (markerSets : Context → Set Gene) (contexts : Finset Context)
    (panel : Finset Gene) : Nat :=
  PanelCoverageCount markerSets contexts panel

/--
Specificity count: the number of negative contexts not hit by the panel.
-/
noncomputable def PanelSpecificityCount {Context Gene : Type} [DecidableEq Context]
    (markerSets : Context → Set Gene) (contexts : Finset Context)
    (panel : Finset Gene) : Nat :=
  (AvoidedContexts markerSets contexts panel).card

/--
The contexts newly covered by adding a gene to an existing panel.
-/
noncomputable def MarginalCoverageContexts {Context Gene : Type} [DecidableEq Context]
    (markerSets : Context → Set Gene) (contexts : Finset Context)
    (panel : Finset Gene) (gene : Gene) : Finset Context := by
  classical
  exact contexts.filter
    (fun context => ¬ PanelHits markerSets panel context ∧ gene ∈ markerSets context)

/--
The marginal coverage gain from adding a gene to an existing panel.
-/
noncomputable def MarginalCoverageCount {Context Gene : Type} [DecidableEq Context]
    (markerSets : Context → Set Gene) (contexts : Finset Context)
    (panel : Finset Gene) (gene : Gene) : Nat :=
  (MarginalCoverageContexts markerSets contexts panel gene).card

/--
Adding genes preserves a hit.
-/
theorem panelHits_mono_genes {Context Gene : Type}
    {markerSets : Context → Set Gene} {panel largerPanel : Finset Gene}
    {context : Context}
    (hsubset : panel ⊆ largerPanel)
    (hhit : PanelHits markerSets panel context) :
    PanelHits markerSets largerPanel context := by
  rcases hhit with ⟨gene, hgene_panel, hgene_marker⟩
  exact ⟨gene, hsubset hgene_panel, hgene_marker⟩

/--
Adding genes can only increase target coverage.
-/
theorem coveredContexts_mono_genes {Context Gene : Type} [DecidableEq Context]
    {markerSets : Context → Set Gene} {contexts : Finset Context}
    {panel largerPanel : Finset Gene}
    (hsubset : panel ⊆ largerPanel) :
    CoveredContexts markerSets contexts panel ⊆
      CoveredContexts markerSets contexts largerPanel := by
  classical
  intro context hcontext
  simp [CoveredContexts] at hcontext ⊢
  exact ⟨hcontext.1, panelHits_mono_genes hsubset hcontext.2⟩

/--
Adding genes can only increase the number of covered positive contexts.
-/
theorem panelCoverageCount_mono_genes {Context Gene : Type} [DecidableEq Context]
    {markerSets : Context → Set Gene} {contexts : Finset Context}
    {panel largerPanel : Finset Gene}
    (hsubset : panel ⊆ largerPanel) :
    PanelCoverageCount markerSets contexts panel ≤
      PanelCoverageCount markerSets contexts largerPanel := by
  exact Finset.card_le_card (coveredContexts_mono_genes hsubset)

/--
Adding genes can only increase the number of off-target contexts hit.
-/
theorem panelOffTargetHitCount_mono_genes {Context Gene : Type} [DecidableEq Context]
    {markerSets : Context → Set Gene} {contexts : Finset Context}
    {panel largerPanel : Finset Gene}
    (hsubset : panel ⊆ largerPanel) :
    PanelOffTargetHitCount markerSets contexts panel ≤
      PanelOffTargetHitCount markerSets contexts largerPanel :=
  panelCoverageCount_mono_genes hsubset

/--
Adding genes can only decrease the number of avoided negative contexts.
-/
theorem panelSpecificityCount_antitone_genes {Context Gene : Type} [DecidableEq Context]
    {markerSets : Context → Set Gene} {contexts : Finset Context}
    {panel largerPanel : Finset Gene}
    (hsubset : panel ⊆ largerPanel) :
    PanelSpecificityCount markerSets contexts largerPanel ≤
      PanelSpecificityCount markerSets contexts panel := by
  classical
  apply Finset.card_le_card
  intro context hcontext
  simp [AvoidedContexts] at hcontext ⊢
  refine ⟨hcontext.1, ?_⟩
  intro hhit
  exact hcontext.2 (panelHits_mono_genes hsubset hhit)

/--
Marginal coverage has diminishing returns: if one panel is contained in a
larger panel, then adding the same gene to the larger panel can cover no more
new contexts than adding it to the smaller panel.
-/
theorem marginalCoverageCount_antitone_panel
    {Context Gene : Type} [DecidableEq Context]
    {markerSets : Context → Set Gene} {contexts : Finset Context}
    {panel largerPanel : Finset Gene} {gene : Gene}
    (hsubset : panel ⊆ largerPanel) :
    MarginalCoverageCount markerSets contexts largerPanel gene ≤
      MarginalCoverageCount markerSets contexts panel gene := by
  classical
  apply Finset.card_le_card
  intro context hcontext
  simp [MarginalCoverageContexts] at hcontext ⊢
  refine ⟨hcontext.1, ?_, hcontext.2.2⟩
  intro hhit
  exact hcontext.2.1 (panelHits_mono_genes hsubset hhit)

/--
A marker panel is feasible when it covers at least a requested number of
positive contexts while hitting at most a requested number of negative contexts.
-/
def SensitivitySpecificityFeasiblePanel {Context Gene : Type} [DecidableEq Context]
    (positiveMarkerSets negativeMarkerSets : Context → Set Gene)
    (positiveContexts negativeContexts : Finset Context)
    (minPositiveCoverage maxOffTargetHits : Nat)
    (panel : Finset Gene) : Prop :=
  PanelCoverageCount positiveMarkerSets positiveContexts panel ≥ minPositiveCoverage ∧
    PanelOffTargetHitCount negativeMarkerSets negativeContexts panel ≤ maxOffTargetHits

/--
Among feasible panels, a minimum feasible panel has minimum cardinality.
-/
def IsMinimumFeasiblePanel {Context Gene : Type} [DecidableEq Context]
    (positiveMarkerSets negativeMarkerSets : Context → Set Gene)
    (positiveContexts negativeContexts : Finset Context)
    (minPositiveCoverage maxOffTargetHits : Nat)
    (panel : Finset Gene) : Prop :=
  SensitivitySpecificityFeasiblePanel positiveMarkerSets negativeMarkerSets
    positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits panel ∧
    ∀ otherPanel : Finset Gene,
      SensitivitySpecificityFeasiblePanel positiveMarkerSets negativeMarkerSets
        positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits otherPanel →
        panel.card ≤ otherPanel.card

/--
Weak Pareto dominance for marker panels: the first panel has at least as much
positive coverage, no more off-target hits, and no more genes than the second.
-/
def PanelWeaklyDominates {Context Gene : Type} [DecidableEq Context]
    (positiveMarkerSets negativeMarkerSets : Context → Set Gene)
    (positiveContexts negativeContexts : Finset Context)
    (better worse : Finset Gene) : Prop :=
  PanelCoverageCount positiveMarkerSets positiveContexts worse ≤
    PanelCoverageCount positiveMarkerSets positiveContexts better ∧
  PanelOffTargetHitCount negativeMarkerSets negativeContexts better ≤
    PanelOffTargetHitCount negativeMarkerSets negativeContexts worse ∧
  better.card ≤ worse.card

/--
Strict Pareto dominance improves at least one of coverage, off-target hits, or
panel size while being no worse on the others.
-/
def PanelStrictlyDominates {Context Gene : Type} [DecidableEq Context]
    (positiveMarkerSets negativeMarkerSets : Context → Set Gene)
    (positiveContexts negativeContexts : Finset Context)
    (better worse : Finset Gene) : Prop :=
  PanelWeaklyDominates positiveMarkerSets negativeMarkerSets
    positiveContexts negativeContexts better worse ∧
  (PanelCoverageCount positiveMarkerSets positiveContexts worse <
      PanelCoverageCount positiveMarkerSets positiveContexts better ∨
    PanelOffTargetHitCount negativeMarkerSets negativeContexts better <
      PanelOffTargetHitCount negativeMarkerSets negativeContexts worse ∨
    better.card < worse.card)

/--
A Pareto-optimal marker panel is not strictly dominated by another panel.
-/
def ParetoOptimalMarkerPanel {Context Gene : Type} [DecidableEq Context]
    (positiveMarkerSets negativeMarkerSets : Context → Set Gene)
    (positiveContexts negativeContexts : Finset Context)
    (panel : Finset Gene) : Prop :=
  ¬ ∃ otherPanel : Finset Gene,
    PanelStrictlyDominates positiveMarkerSets negativeMarkerSets
      positiveContexts negativeContexts otherPanel panel

/--
A panel is drawn from a finite candidate gene universe when every selected gene
belongs to that universe. This is the finite optimization problem used by
marker-panel selection tools.
-/
def PanelWithinGeneUniverse {Gene : Type}
    (candidateGenes panel : Finset Gene) : Prop :=
  panel ⊆ candidateGenes

/--
Pareto optimality restricted to a finite candidate gene universe.
-/
def ParetoOptimalMarkerPanelIn {Context Gene : Type} [DecidableEq Context]
    (candidateGenes : Finset Gene)
    (positiveMarkerSets negativeMarkerSets : Context → Set Gene)
    (positiveContexts negativeContexts : Finset Context)
    (panel : Finset Gene) : Prop :=
  PanelWithinGeneUniverse candidateGenes panel ∧
    ¬ ∃ otherPanel : Finset Gene,
      PanelWithinGeneUniverse candidateGenes otherPanel ∧
        PanelStrictlyDominates positiveMarkerSets negativeMarkerSets
          positiveContexts negativeContexts otherPanel panel

/--
Full positive coverage is the strict marker-panel validity target expressed as a
coverage constraint: every positive context is hit.
-/
def FullPositiveCoveragePanel {Context Gene : Type} [DecidableEq Context]
    (positiveMarkerSets : Context → Set Gene)
    (positiveContexts : Finset Context)
    (panel : Finset Gene) : Prop :=
  PanelCoverageCount positiveMarkerSets positiveContexts panel =
    positiveContexts.card

/--
Full positive coverage is exactly the target-specific marker-panel condition
when positive contexts are the comparison groups and each context's marker set
is its pairwise marker-gene set.
-/
theorem contrastFamilyMarkerPanel_iff_fullPositiveCoveragePanel
    {Study Partition Group Gene : Type} [DecidableEq Group]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {panel : Finset Gene} :
    ContrastFamilyMarkerPanel μ threshold study partition target comparisons panel ↔
      FullPositiveCoveragePanel
        (fun comparison : Group =>
          PairwiseMarkerGenes μ threshold study partition target comparison)
        comparisons panel := by
  rw [contrastFamilyMarkerPanel_iff_hitsPairwiseMarkerSets]
  simp [HitsPairwiseMarkerSets, FullPositiveCoveragePanel, PanelCoverageCount,
    CoveredContexts, PanelHits, Finset.card_filter_eq_iff]

/--
An optimal feasible marker panel is a candidate-universe panel satisfying the
requested sensitivity/specificity constraints that is not strictly dominated by
another feasible panel from the same candidate universe.
-/
def ParetoOptimalFeasibleMarkerPanelIn {Context Gene : Type} [DecidableEq Context]
    (candidateGenes : Finset Gene)
    (positiveMarkerSets negativeMarkerSets : Context → Set Gene)
    (positiveContexts negativeContexts : Finset Context)
    (minPositiveCoverage maxOffTargetHits : Nat)
    (panel : Finset Gene) : Prop :=
  PanelWithinGeneUniverse candidateGenes panel ∧
  SensitivitySpecificityFeasiblePanel positiveMarkerSets negativeMarkerSets
    positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits panel ∧
  ¬ ∃ otherPanel : Finset Gene,
    PanelWithinGeneUniverse candidateGenes otherPanel ∧
    SensitivitySpecificityFeasiblePanel positiveMarkerSets negativeMarkerSets
      positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits otherPanel ∧
    PanelStrictlyDominates positiveMarkerSets negativeMarkerSets
      positiveContexts negativeContexts otherPanel panel

/--
If a feasible marker panel is weakly dominated by another panel, then the
dominating panel is also feasible for the same sensitivity/specificity
constraints. Thus dominated feasible panels can be discarded without losing
feasibility.
-/
theorem feasiblePanel_of_weaklyDominates
    {Context Gene : Type} [DecidableEq Context]
    {positiveMarkerSets negativeMarkerSets : Context → Set Gene}
    {positiveContexts negativeContexts : Finset Context}
    {minPositiveCoverage maxOffTargetHits : Nat}
    {better worse : Finset Gene}
    (hdom :
      PanelWeaklyDominates positiveMarkerSets negativeMarkerSets
        positiveContexts negativeContexts better worse)
    (hfeasible :
      SensitivitySpecificityFeasiblePanel positiveMarkerSets negativeMarkerSets
        positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits worse) :
    SensitivitySpecificityFeasiblePanel positiveMarkerSets negativeMarkerSets
      positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits better := by
  constructor
  · exact le_trans hfeasible.1 hdom.1
  · exact le_trans hdom.2.1 hfeasible.2

/--
A feasible panel that is strictly dominated by another panel is not
Pareto-optimal.
-/
theorem not_paretoOptimalMarkerPanel_of_strictlyDominated
    {Context Gene : Type} [DecidableEq Context]
    {positiveMarkerSets negativeMarkerSets : Context → Set Gene}
    {positiveContexts negativeContexts : Finset Context}
    {better worse : Finset Gene}
    (hdom :
      PanelStrictlyDominates positiveMarkerSets negativeMarkerSets
        positiveContexts negativeContexts better worse) :
    ¬ ParetoOptimalMarkerPanel positiveMarkerSets negativeMarkerSets
      positiveContexts negativeContexts worse := by
  intro hpareto
  exact hpareto ⟨better, hdom⟩

/--
If a panel is strictly dominated by another panel in the same finite candidate
gene universe, then it is not Pareto-optimal in that candidate universe.
-/
theorem not_paretoOptimalMarkerPanelIn_of_strictlyDominated
    {Context Gene : Type} [DecidableEq Context]
    {candidateGenes : Finset Gene}
    {positiveMarkerSets negativeMarkerSets : Context → Set Gene}
    {positiveContexts negativeContexts : Finset Context}
    {better worse : Finset Gene}
    (hbetter : PanelWithinGeneUniverse candidateGenes better)
    (hdom :
      PanelStrictlyDominates positiveMarkerSets negativeMarkerSets
        positiveContexts negativeContexts better worse) :
    ¬ ParetoOptimalMarkerPanelIn candidateGenes positiveMarkerSets negativeMarkerSets
      positiveContexts negativeContexts worse := by
  intro hpareto
  exact hpareto.2 ⟨better, hbetter, hdom⟩

/--
If a feasible panel is strictly dominated by another feasible panel in the same
finite candidate universe, then it is not an optimal feasible marker panel.
-/
theorem not_paretoOptimalFeasibleMarkerPanelIn_of_feasible_strictlyDominated
    {Context Gene : Type} [DecidableEq Context]
    {candidateGenes : Finset Gene}
    {positiveMarkerSets negativeMarkerSets : Context → Set Gene}
    {positiveContexts negativeContexts : Finset Context}
    {minPositiveCoverage maxOffTargetHits : Nat}
    {better worse : Finset Gene}
    (hbetter : PanelWithinGeneUniverse candidateGenes better)
    (hbetter_feasible :
      SensitivitySpecificityFeasiblePanel positiveMarkerSets negativeMarkerSets
        positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits better)
    (hdom :
      PanelStrictlyDominates positiveMarkerSets negativeMarkerSets
        positiveContexts negativeContexts better worse) :
    ¬ ParetoOptimalFeasibleMarkerPanelIn candidateGenes positiveMarkerSets negativeMarkerSets
      positiveContexts negativeContexts minPositiveCoverage maxOffTargetHits worse := by
  intro hpareto
  exact hpareto.2.2 ⟨better, hbetter, hbetter_feasible, hdom⟩

/-!
Marker panels can exist even when the strict marker-gene set is empty. This is
the practical difference between a single marker that must work against every
comparison and a multi-gene panel that can cover different comparisons with
different genes.
-/
namespace MarkerPanelNoStrictMarkerExample

inductive Comparison
  | h₁
  | h₂
  deriving DecidableEq, Fintype

inductive ExampleGene
  | g₁
  | g₂
  deriving DecidableEq, Fintype

def pairwise : Comparison → Set ExampleGene
  | Comparison.h₁ => {ExampleGene.g₁}
  | Comparison.h₂ => {ExampleGene.g₂}

def comparisons : Finset Comparison := {Comparison.h₁, Comparison.h₂}

def panel : Finset ExampleGene := {ExampleGene.g₁, ExampleGene.g₂}

theorem panel_covers_pairwise_sets :
    HitsPairwiseMarkerSets pairwise comparisons panel := by
  intro comparison hcomparison
  fin_cases comparison <;> simp [panel, pairwise]

theorem strict_marker_set_empty :
    (⋂ comparison : {h // h ∈ comparisons}, pairwise comparison.1) =
      (∅ : Set ExampleGene) := by
  ext gene
  fin_cases gene <;> simp [comparisons, pairwise]

theorem panel_without_strict_marker :
    HitsPairwiseMarkerSets pairwise comparisons panel ∧
      (⋂ comparison : {h // h ∈ comparisons}, pairwise comparison.1) =
        (∅ : Set ExampleGene) :=
  ⟨panel_covers_pairwise_sets, strict_marker_set_empty⟩

end MarkerPanelNoStrictMarkerExample

/--
A scoped local group is the local object that can instantiate a cell type claim:
a study, a partition of that study, a target group in the partition, and the
comparison family against which that target is being distinguished.

The biological side condition that the target is not one of its own comparisons
is recorded separately as `ScopedLocalGroup.Valid`, so the structure remains a
plain data object.
-/
structure ScopedLocalGroup (Study Partition Group : Type) where
  study : Study
  partition : Partition
  target : Group
  comparisons : Finset Group

namespace ScopedLocalGroup

/--
A scoped local group is valid when its target is not included in the comparison
family.
-/
def Valid {Study Partition Group : Type} (localGroup : ScopedLocalGroup Study Partition Group) :
    Prop :=
  localGroup.target ∉ localGroup.comparisons

/--
The marker-gene set associated with a scoped local group.
-/
def markerGenes {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (localGroup : ScopedLocalGroup Study Partition Group) : Set Gene :=
  ContrastFamilyMarkerGenes μ threshold localGroup.study localGroup.partition
    localGroup.target localGroup.comparisons

end ScopedLocalGroup

/--
A marker-based cell type claim is supported by the genes that recur across all
of its scoped local instances. This is the marker-evidence component of a cell
type definition, not a full biological ontology.
-/
def SharedMarkerGenes {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (instances : Finset (ScopedLocalGroup Study Partition Group)) : Set Gene :=
  {gene |
    ∀ localGroup : ScopedLocalGroup Study Partition Group, localGroup ∈ instances →
      gene ∈ ScopedLocalGroup.markerGenes μ threshold localGroup}

/--
Membership in the shared marker set is exactly marker recurrence across every
scoped local group of the cell type claim.
-/
theorem mem_sharedMarkerGenes_iff_mem_all_instance_markerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {instances : Finset (ScopedLocalGroup Study Partition Group)} {gene : Gene} :
    gene ∈ SharedMarkerGenes μ threshold instances ↔
      ∀ localGroup : ScopedLocalGroup Study Partition Group, localGroup ∈ instances →
        gene ∈ ScopedLocalGroup.markerGenes μ threshold localGroup := by
  rfl

/--
Adding more local instances to a cell type claim can only shrink the shared
marker set. A marker that works for a broader cross-study claim also works for
any restricted subclaim.
-/
theorem sharedMarkerGenes_subset_of_instances_subset
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {Local Global : Finset (ScopedLocalGroup Study Partition Group)}
    (hsubset : Local ⊆ Global) :
    SharedMarkerGenes μ threshold Global ⊆
      SharedMarkerGenes μ threshold Local := by
  intro gene hglobal localGroup hlocal
  exact hglobal localGroup (hsubset hlocal)

/--
A marker panel is shared across a family of scoped local groups when it covers
the comparison family for every local group in that family.
-/
def SharedMarkerPanel {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (instances : Finset (ScopedLocalGroup Study Partition Group))
    (panel : Finset Gene) : Prop :=
  ∀ localGroup : ScopedLocalGroup Study Partition Group, localGroup ∈ instances →
    ContrastFamilyMarkerPanel μ threshold localGroup.study localGroup.partition
      localGroup.target localGroup.comparisons panel

/--
Adding more local instances makes a shared marker-panel claim harder. A panel
that covers a broader cross-study family of scoped local groups also covers any
restricted subfamily.
-/
theorem sharedMarkerPanel_of_instances_subset
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {Local Global : Finset (ScopedLocalGroup Study Partition Group)}
    {panel : Finset Gene}
    (hsubset : Local ⊆ Global)
    (hglobal : SharedMarkerPanel μ threshold Global panel) :
    SharedMarkerPanel μ threshold Local panel := by
  intro localGroup hlocal
  exact hglobal localGroup (hsubset hlocal)

/--
A singleton shared marker panel is exactly a shared single marker gene.
-/
theorem sharedMarkerPanel_singleton_iff_mem_sharedMarkerGenes
    {Study Partition Group Gene : Type} [DecidableEq Gene]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {instances : Finset (ScopedLocalGroup Study Partition Group)} {gene : Gene} :
    SharedMarkerPanel μ threshold instances ({gene} : Finset Gene) ↔
      gene ∈ SharedMarkerGenes μ threshold instances := by
  constructor
  · intro hpanel localGroup hlocal
    change ContrastFamilyMarker μ threshold localGroup.study localGroup.partition
      localGroup.target localGroup.comparisons gene
    rw [← singleton_contrastFamilyMarkerPanel_iff_contrastFamilyMarker]
    exact hpanel localGroup hlocal
  · intro hshared localGroup hlocal
    rw [singleton_contrastFamilyMarkerPanel_iff_contrastFamilyMarker]
    exact hshared localGroup hlocal

/--
A marker-defined cell type claim consists of a nonempty finite family of scoped
local groups, all valid in the sense that the target is not a comparison group,
and the marker genes shared across those local instances.
-/
structure MarkerDefinedCellType {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ) where
  instances : Finset (ScopedLocalGroup Study Partition Group)
  instances_nonempty : instances.Nonempty
  instances_valid :
    ∀ localGroup : ScopedLocalGroup Study Partition Group, localGroup ∈ instances →
      ScopedLocalGroup.Valid localGroup
  markers : Set Gene
  markers_eq_shared : markers = SharedMarkerGenes μ threshold instances

/--
A gene is in a marker-defined cell type's marker set if and only if it is a
comparison-family marker for every scoped local group of that cell type claim.
-/
theorem mem_markerDefinedCellType_markers_iff_mem_all_instances
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    (cellType : MarkerDefinedCellType μ threshold) {gene : Gene} :
    gene ∈ cellType.markers ↔
      ∀ localGroup : ScopedLocalGroup Study Partition Group, localGroup ∈ cellType.instances →
        ContrastFamilyMarker μ threshold localGroup.study localGroup.partition
          localGroup.target localGroup.comparisons gene := by
  rw [cellType.markers_eq_shared]
  rfl

/--
A marker-panel-defined cell type consists of a nonempty finite family of scoped
local groups and a finite marker panel that covers the comparison family for
each local group. This is the panel-valued analogue of `MarkerDefinedCellType`.
-/
structure MarkerPanelDefinedCellType {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ) where
  instances : Finset (ScopedLocalGroup Study Partition Group)
  instances_nonempty : instances.Nonempty
  instances_valid :
    ∀ localGroup : ScopedLocalGroup Study Partition Group, localGroup ∈ instances →
      ScopedLocalGroup.Valid localGroup
  panel : Finset Gene
  panel_covers : SharedMarkerPanel μ threshold instances panel

/--
If the panel defining a marker-panel-defined cell type is a singleton, then its
gene is shared by every scoped local instance.
-/
theorem markerPanelDefinedCellType_singleton_gene_shared
    {Study Partition Group Gene : Type} [DecidableEq Gene]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    (cellType : MarkerPanelDefinedCellType μ threshold) {gene : Gene}
    (hpanel : cellType.panel = ({gene} : Finset Gene)) :
    gene ∈ SharedMarkerGenes μ threshold cellType.instances := by
  rw [← sharedMarkerPanel_singleton_iff_mem_sharedMarkerGenes]
  rw [← hpanel]
  exact cellType.panel_covers

/--
Every marker of a marker-defined cell type is a marker for each scoped local
group of that cell type.
-/
theorem markerDefinedCellType_markers_subset_instance_markerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    (cellType : MarkerDefinedCellType μ threshold)
    {localGroup : ScopedLocalGroup Study Partition Group}
    (hlocalGroup : localGroup ∈ cellType.instances) :
    cellType.markers ⊆ ScopedLocalGroup.markerGenes μ threshold localGroup := by
  intro gene hgene
  rw [mem_markerDefinedCellType_markers_iff_mem_all_instances] at hgene
  exact hgene localGroup hlocalGroup

/--
Comparison families are ordered by subset inclusion. Moving upward in this
order asks for a marker that works against more comparison groups; moving
downward restricts to a more local biological setting.
-/
def ComparisonFamilyLE {Group : Type} (Local Global : Finset Group) : Prop :=
  Local ⊆ Global

/--
The comparison-family order is reflexive.
-/
theorem comparisonFamilyLE_refl {Group : Type} (C : Finset Group) :
    ComparisonFamilyLE C C := by
  intro h hh
  exact hh

/--
The comparison-family order is transitive.
-/
theorem comparisonFamilyLE_trans {Group : Type} {A B C : Finset Group}
    (hAB : ComparisonFamilyLE A B) (hBC : ComparisonFamilyLE B C) :
    ComparisonFamilyLE A C := by
  intro h hh
  exact hBC (hAB hh)

/--
The comparison-family order is antisymmetric, so finite comparison families form
a partial order under inclusion.
-/
theorem comparisonFamilyLE_antisymm {Group : Type} {A B : Finset Group}
    (hAB : ComparisonFamilyLE A B) (hBA : ComparisonFamilyLE B A) :
    A = B :=
  Finset.Subset.antisymm hAB hBA

/--
For a fixed target, gene, study, partition, and threshold, the comparison
families over which a gene is a marker form a downward-closed set in the
comparison-family poset.
-/
def MarkerComparisonFamilies {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group) (gene : Gene) :
    Set (Finset Group) :=
  {C | ContrastFamilyMarker μ threshold study partition target C gene}

/--
For a fixed target, panel, study, partition, and threshold, the comparison
families over which a panel is valid form a downward-closed set in the
comparison-family poset.
-/
def MarkerPanelComparisonFamilies {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group) (panel : Finset Gene) :
    Set (Finset Group) :=
  {C | ContrastFamilyMarkerPanel μ threshold study partition target C panel}

/--
Restricting the comparison family gives a weaker marker claim. A gene that marks
a target against a broad family also marks that target against any local subset
of comparisons, such as blood immune populations or a disease-specific panel.
-/
theorem contrastFamilyMarker_subset {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {Local Global : Finset Group} {gene : Gene}
    (hsubset : Local ⊆ Global)
    (hglobal : ContrastFamilyMarker μ threshold study partition target Global gene) :
    ContrastFamilyMarker μ threshold study partition target Local gene := by
  intro comparison hlocal
  exact hglobal comparison (hsubset hlocal)

/--
The marker comparison-family set is downward closed in the comparison-family
poset.
-/
theorem markerComparisonFamilies_downward_closed {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group} {gene : Gene}
    {Local Global : Finset Group}
    (hGlobal : Global ∈
      MarkerComparisonFamilies μ threshold study partition target gene)
    (hLocal : ComparisonFamilyLE Local Global) :
    Local ∈ MarkerComparisonFamilies μ threshold study partition target gene :=
  contrastFamilyMarker_subset hLocal hGlobal

/--
The marker-panel comparison-family set is downward closed in the
comparison-family poset.
-/
theorem markerPanelComparisonFamilies_downward_closed
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group} {panel : Finset Gene}
    {Local Global : Finset Group}
    (hGlobal : Global ∈
      MarkerPanelComparisonFamilies μ threshold study partition target panel)
    (hLocal : ComparisonFamilyLE Local Global) :
    Local ∈ MarkerPanelComparisonFamilies μ threshold study partition target panel :=
  contrastFamilyMarkerPanel_subset_comparisons hLocal hGlobal

/--
A hierarchical comparison scope records the relationship between a broader
parent/global comparison family and the local child/sibling comparison family
induced by a refinement of that parent.

No additional tree machinery is needed for the basic marker theorem: the
hierarchy contributes the inclusion proof that the child comparison scope is
contained in the parent comparison scope.
-/
structure HierarchicalComparisonScope (Group : Type) where
  parent : Finset Group
  child : Finset Group
  child_subset_parent : child ⊆ parent

/--
A marker for a target over a parent/global comparison scope is automatically a
marker for the same target over any child/local scope inside that parent.
-/
theorem hierarchical_parent_marker_implies_child_marker
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    (scope : HierarchicalComparisonScope Group) {gene : Gene}
    (hparent :
      ContrastFamilyMarker μ threshold study partition target scope.parent gene) :
    ContrastFamilyMarker μ threshold study partition target scope.child gene :=
  contrastFamilyMarker_subset scope.child_subset_parent hparent

/--
At the marker-set level, the parent/global marker set is contained in the
child/local marker set. Broad hierarchical markers are reusable locally, while
local child markers may include additional genes that fail at the parent scope.
-/
theorem hierarchical_parent_markerGenes_subset_child_markerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    (scope : HierarchicalComparisonScope Group) :
    ContrastFamilyMarkerGenes μ threshold study partition target scope.parent ⊆
      ContrastFamilyMarkerGenes μ threshold study partition target scope.child := by
  intro gene hparent
  exact hierarchical_parent_marker_implies_child_marker scope hparent

/--
A marker panel for a target over a parent/global comparison scope is
automatically a marker panel for the same target over any child/local scope
inside that parent.
-/
theorem hierarchical_parent_markerPanel_implies_child_markerPanel
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    (scope : HierarchicalComparisonScope Group) {panel : Finset Gene}
    (hparent :
      ContrastFamilyMarkerPanel μ threshold study partition target scope.parent panel) :
    ContrastFamilyMarkerPanel μ threshold study partition target scope.child panel :=
  contrastFamilyMarkerPanel_subset_comparisons scope.child_subset_parent hparent

/--
The type/state distinction can be represented as a distinction in comparison
scope. A cell-type scope asks for markers against a broader comparison family;
a cell-state scope restricts that family to the local context, such as sibling
states within a parent cell type or condition.

The target is held fixed in this structure. If the target itself is refined
(for example, T cell to activated T cell), an additional target-refinement map
is needed; that is separate from the comparison-scope theorem below.
-/
structure TypeStateComparisonScope (Group : Type) where
  cellTypeComparisons : Finset Group
  cellStateComparisons : Finset Group
  state_subset_type : cellStateComparisons ⊆ cellTypeComparisons

/--
A marker claim at cell-type scope: the target is distinguished from the broader
cell-type comparison family.
-/
def CellTypeScopeMarker {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (scope : TypeStateComparisonScope Group) (gene : Gene) : Prop :=
  ContrastFamilyMarker μ threshold study partition target
    scope.cellTypeComparisons gene

/--
A marker claim at cell-state scope: the same target is distinguished only from
the restricted local state/context comparison family.
-/
def CellStateScopeMarker {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (scope : TypeStateComparisonScope Group) (gene : Gene) : Prop :=
  ContrastFamilyMarker μ threshold study partition target
    scope.cellStateComparisons gene

/--
At the set level, the cell-type-scope marker genes for a fixed target.
-/
def CellTypeScopeMarkerGenes {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (scope : TypeStateComparisonScope Group) : Set Gene :=
  ContrastFamilyMarkerGenes μ threshold study partition target
    scope.cellTypeComparisons

/--
At the set level, the cell-state-scope marker genes for a fixed target.
-/
def CellStateScopeMarkerGenes {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (scope : TypeStateComparisonScope Group) : Set Gene :=
  ContrastFamilyMarkerGenes μ threshold study partition target
    scope.cellStateComparisons

/--
A marker-panel claim at cell-type scope: the target is distinguished from the
broader cell-type comparison family by at least one selected gene per
comparison.
-/
def CellTypeScopeMarkerPanel {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (scope : TypeStateComparisonScope Group) (panel : Finset Gene) : Prop :=
  ContrastFamilyMarkerPanel μ threshold study partition target
    scope.cellTypeComparisons panel

/--
A marker-panel claim at cell-state scope: the target is distinguished only from
the restricted local state/context comparison family by the selected panel.
-/
def CellStateScopeMarkerPanel {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (scope : TypeStateComparisonScope Group) (panel : Finset Gene) : Prop :=
  ContrastFamilyMarkerPanel μ threshold study partition target
    scope.cellStateComparisons panel

/--
For a fixed target, any marker valid at the broader cell-type comparison scope
is valid at the restricted cell-state scope.
-/
theorem cellTypeScopeMarker_implies_cellStateScopeMarker
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    (scope : TypeStateComparisonScope Group) {gene : Gene}
    (htype :
      CellTypeScopeMarker μ threshold study partition target scope gene) :
    CellStateScopeMarker μ threshold study partition target scope gene :=
  contrastFamilyMarker_subset scope.state_subset_type htype

/--
For a fixed target, the type-scope marker set is contained in the state-scope
marker set whenever the state comparison family is a restriction of the type
comparison family.
-/
theorem cellTypeScopeMarkerGenes_subset_cellStateScopeMarkerGenes
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    (scope : TypeStateComparisonScope Group) :
    CellTypeScopeMarkerGenes μ threshold study partition target scope ⊆
      CellStateScopeMarkerGenes μ threshold study partition target scope := by
  intro gene htype
  exact cellTypeScopeMarker_implies_cellStateScopeMarker scope htype

/--
For a fixed target, any marker panel valid at the broader cell-type comparison
scope is valid at the restricted cell-state scope.
-/
theorem cellTypeScopeMarkerPanel_implies_cellStateScopeMarkerPanel
    {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    (scope : TypeStateComparisonScope Group) {panel : Finset Gene}
    (htype :
      CellTypeScopeMarkerPanel μ threshold study partition target scope panel) :
    CellStateScopeMarkerPanel μ threshold study partition target scope panel :=
  contrastFamilyMarkerPanel_subset_comparisons scope.state_subset_type htype

/--
Necessary and sufficient condition for a comparison-family marker: a gene marks
the target relative to a comparison family if and only if it recurs as a
one-vs-background marker against every singleton background drawn from that
family. This makes the comparison family part of the marker definition.
-/
theorem contrastFamilyMarker_iff_singleton_background_markers
    {Study Partition Group Gene : Type} [DecidableEq Group]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {gene : Gene} :
    ContrastFamilyMarker μ threshold study partition target comparisons gene ↔
      ∀ comparison : Group, comparison ∈ comparisons →
        BackgroundContrastMarker μ threshold study partition target
          ({comparison} : Finset Group) (fun _ => 1) gene := by
  constructor
  · intro hfamily comparison hcomparison
    have hpair := hfamily comparison hcomparison
    simpa [BackgroundContrastMarker, LocalBackgroundContrast,
      PairwiseContrastMarker, LocalPairwiseContrast] using hpair
  · intro hbackground comparison hcomparison
    have hsingle := hbackground comparison hcomparison
    simpa [BackgroundContrastMarker, LocalBackgroundContrast,
      PairwiseContrastMarker, LocalPairwiseContrast] using hsingle

/-- Non-strict pairwise marker predicate, useful for convex-background theorems. -/
def PairwiseContrastMarkerGE {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition)
    (target comparison : Group) (gene : Gene) : Prop :=
  threshold ≤ LocalPairwiseContrast μ study partition target comparison gene

/-- Non-strict one-vs-background marker predicate. -/
def BackgroundContrastMarkerGE {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (background : Finset Group) (w : Group → ℝ) (gene : Gene) : Prop :=
  threshold ≤ LocalBackgroundContrast μ study partition target background w gene

/--
Nonnegative weights on a finite background that sum to one.
-/
def NormalizedNonnegativeWeights {Group : Type}
    (background : Finset Group) (w : Group → ℝ) : Prop :=
  (∀ h : Group, h ∈ background → 0 ≤ w h) ∧
    (∑ h ∈ background, w h) = 1

/--
Non-strict comparison-family marker predicate: the gene clears the threshold
against every comparison group in the family.
-/
def ContrastFamilyMarkerGE {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (comparisons : Finset Group) (gene : Gene) : Prop :=
  ∀ comparison : Group, comparison ∈ comparisons →
    PairwiseContrastMarkerGE μ threshold study partition target comparison gene

/--
The non-strict contrast-family marker predicate is also weakened by restricting
the comparison family.
-/
theorem contrastFamilyMarkerGE_subset {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {Local Global : Finset Group} {gene : Gene}
    (hsubset : Local ⊆ Global)
    (hglobal : ContrastFamilyMarkerGE μ threshold study partition target Global gene) :
    ContrastFamilyMarkerGE μ threshold study partition target Local gene := by
  intro comparison hlocal
  exact hglobal comparison (hsubset hlocal)

/--
Necessary and sufficient condition for a background-robust marker.

A gene clears the threshold against every pairwise comparison in a comparison
family if and only if it clears the same threshold for every normalized
nonnegative one-vs-background contrast whose background is drawn from that
family. The forward direction says pairwise recurrence is sufficient for any
chosen background; the reverse direction follows because singleton backgrounds
are valid normalized backgrounds.
-/
theorem contrastFamilyMarkerGE_iff_all_normalized_background_markers
    {Study Partition Group Gene : Type} [DecidableEq Group]
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {comparisons : Finset Group} {gene : Gene} :
    ContrastFamilyMarkerGE μ threshold study partition target comparisons gene ↔
      ∀ background : Finset Group, background ⊆ comparisons →
        ∀ w : Group → ℝ, NormalizedNonnegativeWeights background w →
          BackgroundContrastMarkerGE μ threshold study partition target background w gene := by
  constructor
  · intro hfamily background hbackground w hw
    dsimp [BackgroundContrastMarkerGE]
    rw [localBackgroundContrast_eq_weighted_pairwise
      (μ := μ) (study := study) (partition := partition) (target := target)
      (background := background) (w := w) (gene := gene) hw.2]
    calc
      threshold = (∑ h ∈ background, w h) * threshold := by
        rw [hw.2]
        ring
      _ = ∑ h ∈ background, w h * threshold := by
        rw [Finset.sum_mul]
      _ ≤ ∑ h ∈ background,
            w h * LocalPairwiseContrast μ study partition target h gene := by
        apply Finset.sum_le_sum
        intro h hh
        exact mul_le_mul_of_nonneg_left (hfamily h (hbackground hh)) (hw.1 h hh)
  · intro hbackgrounds comparison hcomparison
    dsimp [PairwiseContrastMarkerGE]
    have hsubset : ({comparison} : Finset Group) ⊆ comparisons := by
      intro h hh
      simp at hh
      subst h
      exact hcomparison
    have hweights : NormalizedNonnegativeWeights
        ({comparison} : Finset Group) (fun _ : Group => (1 : ℝ)) := by
      constructor
      · intro h _hh
        norm_num
      · simp
    have hbackground := hbackgrounds ({comparison} : Finset Group)
      hsubset (fun _ : Group => (1 : ℝ)) hweights
    simpa [BackgroundContrastMarkerGE, LocalBackgroundContrast,
      PairwiseContrastMarkerGE, LocalPairwiseContrast] using hbackground

/-!
## Real-valued marker scores and thresholded marker claims

The main marker definition assumes binary marker calls. A real-valued marker
score becomes such a call only after a decision rule, here represented by a
threshold. The comparison-scope algebra is unchanged after this thresholding:
the family-level marker set is still the intersection of thresholded pairwise
marker sets.
-/

/-- A real-valued pairwise marker score for one target against each comparison. -/
abbrev PairwiseMarkerScore (Group Gene : Type) := Group → Gene → ℝ

/-- A gene is a pairwise marker when its real-valued score clears a threshold. -/
def ScorePairwiseMarker {Group Gene : Type}
    (score : PairwiseMarkerScore Group Gene) (threshold : ℝ)
    (comparison : Group) (gene : Gene) : Prop :=
  threshold ≤ score comparison gene

/-- The thresholded pairwise marker set induced by a real-valued score. -/
def ScorePairwiseMarkerGenes {Group Gene : Type}
    (score : PairwiseMarkerScore Group Gene) (threshold : ℝ)
    (comparison : Group) : Set Gene :=
  {gene | ScorePairwiseMarker score threshold comparison gene}

/--
A gene is a scored marker for a comparison family when it clears the threshold
against every comparison in that family.
-/
def ScoreFamilyMarker {Group Gene : Type}
    (score : PairwiseMarkerScore Group Gene) (threshold : ℝ)
    (comparisons : Finset Group) (gene : Gene) : Prop :=
  ∀ comparison : Group, comparison ∈ comparisons →
    ScorePairwiseMarker score threshold comparison gene

/-- The scored marker-gene set for a finite comparison family. -/
def ScoreFamilyMarkerGenes {Group Gene : Type}
    (score : PairwiseMarkerScore Group Gene) (threshold : ℝ)
    (comparisons : Finset Group) : Set Gene :=
  {gene | ScoreFamilyMarker score threshold comparisons gene}

/--
Thresholded real-valued score markers satisfy the same marker-family axioms as
binary pairwise marker calls.
-/
theorem scoreFamilyMarkerGenes_satisfies_markerFamilyAxioms
    {Group Gene : Type} [DecidableEq Group]
    {score : PairwiseMarkerScore Group Gene} {threshold : ℝ} :
    MarkerFamilyAxioms
      (fun comparison : Group => ScorePairwiseMarkerGenes score threshold comparison)
      (fun comparisons : Finset Group => ScoreFamilyMarkerGenes score threshold comparisons) := by
  refine ⟨?empty, ?singleton, ?union⟩
  · ext gene
    simp [ScoreFamilyMarkerGenes, ScoreFamilyMarker]
  · intro comparison
    ext gene
    simp [ScoreFamilyMarkerGenes, ScoreFamilyMarker, ScorePairwiseMarkerGenes,
      ScorePairwiseMarker]
  · intro C D
    ext gene
    simp only [ScoreFamilyMarkerGenes, ScoreFamilyMarker, Set.mem_setOf_eq,
      Set.mem_inter_iff, Finset.mem_union]
    constructor
    · intro hmarker
      constructor
      · intro comparison hcomparison
        exact hmarker comparison (Or.inl hcomparison)
      · intro comparison hcomparison
        exact hmarker comparison (Or.inr hcomparison)
    · intro hmarker comparison hcomparison
      rcases hcomparison with hcomparison | hcomparison
      · exact hmarker.1 comparison hcomparison
      · exact hmarker.2 comparison hcomparison

/--
Membership in a thresholded scored marker family is equivalent to membership in
every thresholded pairwise marker set.
-/
theorem mem_scoreFamilyMarkerGenes_iff_mem_all_pairwiseMarkerGenes
    {Group Gene : Type}
    {score : PairwiseMarkerScore Group Gene} {threshold : ℝ}
    {comparisons : Finset Group} {gene : Gene} :
    gene ∈ ScoreFamilyMarkerGenes score threshold comparisons ↔
      ∀ comparison : Group, comparison ∈ comparisons →
        gene ∈ ScorePairwiseMarkerGenes score threshold comparison := by
  rfl

/--
The thresholded scored marker set for a comparison family is the intersection of
the thresholded pairwise scored marker sets.
-/
theorem scoreFamilyMarkerGenes_eq_iInter_pairwiseMarkerGenes
    {Group Gene : Type}
    {score : PairwiseMarkerScore Group Gene} {threshold : ℝ}
    {comparisons : Finset Group} :
    ScoreFamilyMarkerGenes score threshold comparisons =
      ⋂ comparison : {h // h ∈ comparisons},
        ScorePairwiseMarkerGenes score threshold comparison.1 := by
  ext gene
  simp [ScoreFamilyMarkerGenes, ScoreFamilyMarker, ScorePairwiseMarkerGenes,
    ScorePairwiseMarker]

/--
Raising the score threshold can only remove marker genes for a fixed comparison
family.
-/
theorem scoreFamilyMarkerGenes_antitone_threshold
    {Group Gene : Type}
    {score : PairwiseMarkerScore Group Gene}
    {threshold_low threshold_high : ℝ}
    {comparisons : Finset Group}
    (hthreshold : threshold_low ≤ threshold_high) :
    ScoreFamilyMarkerGenes score threshold_high comparisons ⊆
      ScoreFamilyMarkerGenes score threshold_low comparisons := by
  intro gene hhigh comparison hcomparison
  exact hthreshold.trans (hhigh comparison hcomparison)

/-!
## Atlas-facing consequences

The following definitions and theorems make explicit several practical atlas
building consequences of the comparison-relative marker definition.
-/

/--
A specific unordered or ordered pair is covered by a collection of local
experiments if both endpoints appear together in at least one experiment.
-/
def PairObservedInExperiments [DecidableEq Cell]
    (Experiments : Finset (Finset Cell)) (c₁ c₂ : Cell) : Prop :=
  ∃ E : Finset Cell, E ∈ Experiments ∧ c₁ ∈ E ∧ c₂ ∈ E

/--
A marker panel certifies a pair from a collection of experiments if the pair
appears in some local experiment that is separated by the panel.
-/
def PairCertifiableByExperiments [DecidableEq Cell] [DecidableEq Gene]
    (X : MarkerMatrix Cell Gene) (S : Finset Gene)
    (Experiments : Finset (Finset Cell)) (c₁ c₂ : Cell) : Prop :=
  ∃ E : Finset Cell, E ∈ Experiments ∧ c₁ ∈ E ∧ c₂ ∈ E ∧ c₁ ≠ c₂ ∧
    SeparatesOn X S E

/--
An uncovered pair cannot be certified from the observed local experiments alone.
This is the formal identifiability gap: if no study ever compares two target
profiles, local-study evidence cannot certify a marker panel for that pair.
-/
theorem not_pairCertifiable_of_not_observed [DecidableEq Cell] [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene}
    {Experiments : Finset (Finset Cell)} {c₁ c₂ : Cell}
    (hunobserved : ¬ PairObservedInExperiments Experiments c₁ c₂) :
    ¬ PairCertifiableByExperiments X S Experiments c₁ c₂ := by
  intro hcert
  rcases hcert with ⟨E, hE, hc₁E, hc₂E, _hne, _hsep⟩
  exact hunobserved ⟨E, hE, hc₁E, hc₂E⟩

/--
A reported pairwise marker predicate. The first group is the target, the second
group is the comparison/background group, and the gene is the proposed marker.
Different statistical pipelines can instantiate this predicate in different
ways; the results below only use the reported pairwise relation.
-/
abbrev PairwiseMarkerPredicate (Group Gene : Type) := Group → Group → Gene → Prop

/--
The local comparison family available for each target group. In a study, this
is the list of target-versus-background groups that were actually reported for
that target.
-/
abbrev LocalComparisonFamily (Group : Type) := Group → Finset Group

/--
A gene is a local family marker for a target when it is a pairwise marker
against every reported comparison group in that target's local family.
-/
def LocalFamilyMarker {Group Gene : Type}
    (pairwise : PairwiseMarkerPredicate Group Gene)
    (comparisons : LocalComparisonFamily Group)
    (target : Group) (gene : Gene) : Prop :=
  ∀ comparison : Group, comparison ∈ comparisons target →
    pairwise target comparison gene

/--
A recurrent local marker for label `L` is a gene that is a local family marker
for every observed target group carrying label `L`.
-/
def RecurrentLocalMarker {Group Label Gene : Type}
    (label : Group → Label) (targets : Finset Group)
    (comparisons : LocalComparisonFamily Group)
    (pairwise : PairwiseMarkerPredicate Group Gene)
    (L : Label) (gene : Gene) : Prop :=
  ∀ target : Group, target ∈ targets → label target = L →
    LocalFamilyMarker pairwise comparisons target gene

/--
A certified global marker for label `L` is a gene that marks every observed
target group carrying `L` against every group in the chosen global background
that does not carry `L`.
-/
def CertifiedGlobalMarker {Group Label Gene : Type}
    (label : Group → Label) (targets background : Finset Group)
    (pairwise : PairwiseMarkerPredicate Group Gene)
    (L : Label) (gene : Gene) : Prop :=
  ∀ target : Group, target ∈ targets → label target = L →
    ∀ comparison : Group, comparison ∈ background → label comparison ≠ L →
      pairwise target comparison gene

/--
The target-background pair coverage needed to turn recurrent local marker
evidence into a certified global marker. For every target instance carrying
label `L`, every required global background group with a different label must
appear in that target's reported local comparison family.
-/
def TargetBackgroundPairCovered {Group Label : Type}
    (label : Group → Label) (targets background : Finset Group)
    (comparisons : LocalComparisonFamily Group) (L : Label) : Prop :=
  ∀ target : Group, target ∈ targets → label target = L →
    ∀ comparison : Group, comparison ∈ background → label comparison ≠ L →
      comparison ∈ comparisons target

/--
If a global marker has already been certified, then it is recurrent locally for
any reported local comparison families that are contained in the same global
background and exclude groups with the target label.
-/
theorem certifiedGlobalMarker_implies_recurrentLocalMarker
    {Group Label Gene : Type}
    {label : Group → Label} {targets background : Finset Group}
    {comparisons : LocalComparisonFamily Group}
    {pairwise : PairwiseMarkerPredicate Group Gene}
    {L : Label} {gene : Gene}
    (hlocal :
      ∀ target : Group, target ∈ targets → label target = L →
        ∀ comparison : Group, comparison ∈ comparisons target →
          comparison ∈ background ∧ label comparison ≠ L)
    (hglobal :
      CertifiedGlobalMarker label targets background pairwise L gene) :
    RecurrentLocalMarker label targets comparisons pairwise L gene := by
  intro target htarget hlabel comparison hcomparison
  exact hglobal target htarget hlabel comparison
    (hlocal target htarget hlabel comparison hcomparison).1
    (hlocal target htarget hlabel comparison hcomparison).2

/--
Recurrent local evidence certifies a global marker exactly when the reported
local comparison families cover all target-background pairs required by the
global marker statement.
-/
theorem certifiedGlobalMarker_of_recurrentLocalMarker_pairCovered
    {Group Label Gene : Type}
    {label : Group → Label} {targets background : Finset Group}
    {comparisons : LocalComparisonFamily Group}
    {pairwise : PairwiseMarkerPredicate Group Gene}
    {L : Label} {gene : Gene}
    (hcover : TargetBackgroundPairCovered label targets background comparisons L)
    (hrecurrent :
      RecurrentLocalMarker label targets comparisons pairwise L gene) :
    CertifiedGlobalMarker label targets background pairwise L gene := by
  intro target htarget hlabel comparison hcomparison hcomparison_label
  exact hrecurrent target htarget hlabel comparison
    (hcover target htarget hlabel comparison hcomparison hcomparison_label)

/--
When local comparison families are exactly the required target-background
comparisons, recurrent local markers and certified global markers coincide.
-/
theorem recurrentLocalMarker_iff_certifiedGlobalMarker_of_exact_pairCoverage
    {Group Label Gene : Type}
    {label : Group → Label} {targets background : Finset Group}
    {comparisons : LocalComparisonFamily Group}
    {pairwise : PairwiseMarkerPredicate Group Gene}
    {L : Label} {gene : Gene}
    (hlocal :
      ∀ target : Group, target ∈ targets → label target = L →
        ∀ comparison : Group, comparison ∈ comparisons target →
          comparison ∈ background ∧ label comparison ≠ L)
    (hcover : TargetBackgroundPairCovered label targets background comparisons L) :
    RecurrentLocalMarker label targets comparisons pairwise L gene ↔
      CertifiedGlobalMarker label targets background pairwise L gene := by
  constructor
  · exact certifiedGlobalMarker_of_recurrentLocalMarker_pairCovered hcover
  · exact certifiedGlobalMarker_implies_recurrentLocalMarker hlocal

/--
A marker panel is a local family panel for a target when every reported
comparison group in that target's local family is covered by at least one gene
in the panel.
-/
def LocalFamilyMarkerPanel {Group Gene : Type}
    (pairwise : PairwiseMarkerPredicate Group Gene)
    (comparisons : LocalComparisonFamily Group)
    (target : Group) (panel : Finset Gene) : Prop :=
  ∀ comparison : Group, comparison ∈ comparisons target →
    ∃ gene : Gene, gene ∈ panel ∧ pairwise target comparison gene

/--
A recurrent local marker panel for label `L` covers every reported local
comparison family for every observed target group carrying label `L`.
-/
def RecurrentLocalMarkerPanel {Group Label Gene : Type}
    (label : Group → Label) (targets : Finset Group)
    (comparisons : LocalComparisonFamily Group)
    (pairwise : PairwiseMarkerPredicate Group Gene)
    (L : Label) (panel : Finset Gene) : Prop :=
  ∀ target : Group, target ∈ targets → label target = L →
    LocalFamilyMarkerPanel pairwise comparisons target panel

/--
A certified global marker panel for label `L` covers every observed target group
carrying `L` against every group in the chosen global background whose label is
not `L`.
-/
def CertifiedGlobalMarkerPanel {Group Label Gene : Type}
    (label : Group → Label) (targets background : Finset Group)
    (pairwise : PairwiseMarkerPredicate Group Gene)
    (L : Label) (panel : Finset Gene) : Prop :=
  ∀ target : Group, target ∈ targets → label target = L →
    ∀ comparison : Group, comparison ∈ background → label comparison ≠ L →
      ∃ gene : Gene, gene ∈ panel ∧ pairwise target comparison gene

/--
If a global marker panel has already been certified, then it is recurrent
locally for any reported local comparison families contained in the same global
background and excluding groups with the target label.
-/
theorem certifiedGlobalMarkerPanel_implies_recurrentLocalMarkerPanel
    {Group Label Gene : Type}
    {label : Group → Label} {targets background : Finset Group}
    {comparisons : LocalComparisonFamily Group}
    {pairwise : PairwiseMarkerPredicate Group Gene}
    {L : Label} {panel : Finset Gene}
    (hlocal :
      ∀ target : Group, target ∈ targets → label target = L →
        ∀ comparison : Group, comparison ∈ comparisons target →
          comparison ∈ background ∧ label comparison ≠ L)
    (hglobal :
      CertifiedGlobalMarkerPanel label targets background pairwise L panel) :
    RecurrentLocalMarkerPanel label targets comparisons pairwise L panel := by
  intro target htarget hlabel comparison hcomparison
  exact hglobal target htarget hlabel comparison
    (hlocal target htarget hlabel comparison hcomparison).1
    (hlocal target htarget hlabel comparison hcomparison).2

/--
Recurrent local marker-panel evidence certifies a global marker panel when the
reported local comparison families cover all target-background pairs required by
the global marker-panel statement.
-/
theorem certifiedGlobalMarkerPanel_of_recurrentLocalMarkerPanel_pairCovered
    {Group Label Gene : Type}
    {label : Group → Label} {targets background : Finset Group}
    {comparisons : LocalComparisonFamily Group}
    {pairwise : PairwiseMarkerPredicate Group Gene}
    {L : Label} {panel : Finset Gene}
    (hcover : TargetBackgroundPairCovered label targets background comparisons L)
    (hrecurrent :
      RecurrentLocalMarkerPanel label targets comparisons pairwise L panel) :
    CertifiedGlobalMarkerPanel label targets background pairwise L panel := by
  intro target htarget hlabel comparison hcomparison hcomparison_label
  exact hrecurrent target htarget hlabel comparison
    (hcover target htarget hlabel comparison hcomparison hcomparison_label)

/--
When local comparison families are exactly the required target-background
comparisons, recurrent local marker panels and certified global marker panels
coincide.
-/
theorem recurrentLocalMarkerPanel_iff_certifiedGlobalMarkerPanel_of_exact_pairCoverage
    {Group Label Gene : Type}
    {label : Group → Label} {targets background : Finset Group}
    {comparisons : LocalComparisonFamily Group}
    {pairwise : PairwiseMarkerPredicate Group Gene}
    {L : Label} {panel : Finset Gene}
    (hlocal :
      ∀ target : Group, target ∈ targets → label target = L →
        ∀ comparison : Group, comparison ∈ comparisons target →
          comparison ∈ background ∧ label comparison ≠ L)
    (hcover : TargetBackgroundPairCovered label targets background comparisons L) :
    RecurrentLocalMarkerPanel label targets comparisons pairwise L panel ↔
      CertifiedGlobalMarkerPanel label targets background pairwise L panel := by
  constructor
  · exact certifiedGlobalMarkerPanel_of_recurrentLocalMarkerPanel_pairCovered hcover
  · exact certifiedGlobalMarkerPanel_implies_recurrentLocalMarkerPanel hlocal

/--
A context-specific marker is valid for a restricted comparison family but not
for a broader comparison family that contains it.
-/
def ContextSpecificMarker {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (Local Global : Finset Group) (gene : Gene) : Prop :=
  Local ⊆ Global ∧
    ContrastFamilyMarker μ threshold study partition target Local gene ∧
      ¬ ContrastFamilyMarker μ threshold study partition target Global gene

theorem contextSpecificMarker_local {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {Local Global : Finset Group} {gene : Gene}
    (h : ContextSpecificMarker μ threshold study partition target Local Global gene) :
    ContrastFamilyMarker μ threshold study partition target Local gene :=
  h.2.1

theorem contextSpecificMarker_not_global {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {Local Global : Finset Group} {gene : Gene}
    (h : ContextSpecificMarker μ threshold study partition target Local Global gene) :
    ¬ ContrastFamilyMarker μ threshold study partition target Global gene :=
  h.2.2

/--
A hierarchy-specific marker is a child/local marker that does not lift to the
parent/global comparison scope.
-/
def HierarchySpecificMarker {Study Partition Group Gene : Type}
    (μ : LocalMeanProfile Study Partition Group Gene) (threshold : ℝ)
    (study : Study) (partition : Partition) (target : Group)
    (scope : HierarchicalComparisonScope Group) (gene : Gene) : Prop :=
  ContextSpecificMarker μ threshold study partition target scope.child scope.parent gene

theorem hierarchySpecificMarker_child {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {scope : HierarchicalComparisonScope Group} {gene : Gene}
    (h : HierarchySpecificMarker μ threshold study partition target scope gene) :
    ContrastFamilyMarker μ threshold study partition target scope.child gene :=
  contextSpecificMarker_local h

theorem hierarchySpecificMarker_not_parent {Study Partition Group Gene : Type}
    {μ : LocalMeanProfile Study Partition Group Gene} {threshold : ℝ}
    {study : Study} {partition : Partition} {target : Group}
    {scope : HierarchicalComparisonScope Group} {gene : Gene}
    (h : HierarchySpecificMarker μ threshold study partition target scope gene) :
    ¬ ContrastFamilyMarker μ threshold study partition target scope.parent gene :=
  contextSpecificMarker_not_global h

/--
A scalar contrast observation clears a threshold in every study in a finite
study set.
-/
def ReproducibleScalarMarkerGE {Study : Type}
    (δ : Study → ℝ) (threshold : ℝ) (studies : Finset Study) : Prop :=
  ∀ study : Study, study ∈ studies → threshold ≤ δ study

/--
Reproducibility over studies is downward closed: if a contrast clears the
threshold in a larger study collection, it clears it in every subset.
-/
theorem reproducibleScalarMarkerGE_subset {Study : Type}
    {δ : Study → ℝ} {threshold : ℝ} {LocalStudies GlobalStudies : Finset Study}
    (hsubset : LocalStudies ⊆ GlobalStudies)
    (hglobal : ReproducibleScalarMarkerGE δ threshold GlobalStudies) :
    ReproducibleScalarMarkerGE δ threshold LocalStudies := by
  intro study hstudy
  exact hglobal study (hsubset hstudy)

/--
If every observed local contrast is within `η` of a global estimate, and the
estimate remains at least `η` above the marker threshold, then the gene clears
the threshold in every observed study. This is a deterministic version of a
low-heterogeneity reproducibility criterion.
-/
theorem reproducibleScalarMarkerGE_of_uniform_estimate_margin {Study : Type}
    {δ : Study → ℝ} {threshold estimate η : ℝ} {studies : Finset Study}
    (hestimate : ∀ study : Study, study ∈ studies → |δ study - estimate| ≤ η)
    (hmargin : threshold ≤ estimate - η) :
    ReproducibleScalarMarkerGE δ threshold studies := by
  intro study hstudy
  have hleft := (abs_le.mp (hestimate study hstudy)).1
  linarith

/--
Labels are a separate projection of local groups. Two groups have the same label
when the label map assigns them the same value.
-/
def SameLabel {Group Label : Type} (label : Group → Label) (g₁ g₂ : Group) : Prop :=
  label g₁ = label g₂

/--
Same labels alone do not force the selected marker signature to agree. This is a
small witness for label insufficiency: a biological label can collapse two
profiles that a marker gene still distinguishes.
-/
theorem sameLabel_does_not_force_sameOn :
    ∃ (label : Bool → Bool) (X : MarkerMatrix Bool Bool) (S : Finset Bool)
      (g₁ g₂ : Bool),
      SameLabel label g₁ g₂ ∧ ¬ SameOn X S g₁ g₂ := by
  let label : Bool → Bool := fun _ => true
  let X : MarkerMatrix Bool Bool := fun group gene => group && gene
  refine ⟨label, X, ({true} : Finset Bool), true, false, ?_⟩
  constructor
  · rfl
  · intro hsame
    have h := hsame true (by simp)
    norm_num [X] at h

/-!
Local recurrence without target-background pair coverage does not identify a
global marker. The same target label can have a marker in every reported local
comparison, while the gene fails against an unreported global background group.
-/
namespace RecurrentLocalNotGlobalExample

inductive Group
  | target
  | localBackground
  | unseenBackground
  deriving DecidableEq

inductive Label
  | targetLabel
  | backgroundLabel
  deriving DecidableEq

inductive ExampleGene
  | marker
  deriving DecidableEq

def label : Group → Label
  | Group.target => Label.targetLabel
  | Group.localBackground => Label.backgroundLabel
  | Group.unseenBackground => Label.backgroundLabel

def targets : Finset Group := {Group.target}

def background : Finset Group := {Group.localBackground, Group.unseenBackground}

def comparisons : LocalComparisonFamily Group
  | Group.target => {Group.localBackground}
  | Group.localBackground => ∅
  | Group.unseenBackground => ∅

def goodPairwise : PairwiseMarkerPredicate Group ExampleGene
  | Group.target, Group.localBackground, ExampleGene.marker => True
  | Group.target, Group.unseenBackground, ExampleGene.marker => True
  | _, _, _ => False

def badPairwise : PairwiseMarkerPredicate Group ExampleGene
  | Group.target, Group.localBackground, ExampleGene.marker => True
  | Group.target, Group.unseenBackground, ExampleGene.marker => False
  | _, _, _ => False

theorem recurrent_good :
    RecurrentLocalMarker label targets comparisons goodPairwise
      Label.targetLabel ExampleGene.marker := by
  intro tgt htarget _hlabel comparison hcomparison
  have htarget_eq : tgt = Group.target := by
    simpa [targets] using htarget
  subst tgt
  have hcomparison_eq : comparison = Group.localBackground := by
    simpa [comparisons] using hcomparison
  subst comparison
  simp [goodPairwise]

theorem recurrent_bad :
    RecurrentLocalMarker label targets comparisons badPairwise
      Label.targetLabel ExampleGene.marker := by
  intro tgt htarget _hlabel comparison hcomparison
  have htarget_eq : tgt = Group.target := by
    simpa [targets] using htarget
  subst tgt
  have hcomparison_eq : comparison = Group.localBackground := by
    simpa [comparisons] using hcomparison
  subst comparison
  simp [badPairwise]

theorem good_certifiedGlobal :
    CertifiedGlobalMarker label targets background goodPairwise
      Label.targetLabel ExampleGene.marker := by
  intro tgt htarget _hlabel comparison hcomparison _hcomparison_label
  have htarget_eq : tgt = Group.target := by
    simpa [targets] using htarget
  subst tgt
  have hcomparison_cases :
      comparison = Group.localBackground ∨ comparison = Group.unseenBackground := by
    simpa [background] using hcomparison
  rcases hcomparison_cases with rfl | rfl <;> simp [goodPairwise]

theorem bad_not_certifiedGlobal :
    ¬ CertifiedGlobalMarker label targets background badPairwise
      Label.targetLabel ExampleGene.marker := by
  intro hglobal
  have hbad := hglobal Group.target (by simp [targets]) rfl
    Group.unseenBackground (by simp [background]) (by simp [label])
  simp [badPairwise] at hbad

theorem not_pairCovered :
    ¬ TargetBackgroundPairCovered label targets background comparisons
      Label.targetLabel := by
  intro hcover
  have hunseen := hcover Group.target (by simp [targets]) rfl
    Group.unseenBackground (by simp [background]) (by simp [label])
  simp [comparisons] at hunseen

theorem recurrentLocal_does_not_certify_global_without_pairCoverage :
    RecurrentLocalMarker label targets comparisons badPairwise
      Label.targetLabel ExampleGene.marker ∧
      ¬ CertifiedGlobalMarker label targets background badPairwise
        Label.targetLabel ExampleGene.marker ∧
      ¬ TargetBackgroundPairCovered label targets background comparisons
        Label.targetLabel := by
  exact ⟨recurrent_bad, bad_not_certifiedGlobal, not_pairCovered⟩

end RecurrentLocalNotGlobalExample

/--
An ontology- or label-derived comparison family is the subset of a group
universe whose mapped terms lie in a chosen term family.
-/
def OntologyComparisonFamily {Group Ontology : Type} [DecidableEq Ontology]
    (ontology : Group → Ontology) (groupUniverse : Finset Group)
    (terms : Finset Ontology) : Finset Group :=
  groupUniverse.filter (fun group => ontology group ∈ terms)

/--
Broadening an ontology term set broadens the induced comparison family.
-/
theorem ontologyComparisonFamily_mono {Group Ontology : Type} [DecidableEq Ontology]
    {ontology : Group → Ontology} {groupUniverse : Finset Group}
    {LocalTerms GlobalTerms : Finset Ontology}
    (hterms : LocalTerms ⊆ GlobalTerms) :
    OntologyComparisonFamily ontology groupUniverse LocalTerms ⊆
      OntologyComparisonFamily ontology groupUniverse GlobalTerms := by
  intro group hgroup
  simp [OntologyComparisonFamily] at hgroup ⊢
  exact ⟨hgroup.1, hterms hgroup.2⟩

/--
Marker separation restricted to the confusable-neighbor graph around a target.
-/
def SeparatesTargetNeighbors [DecidableEq Gene]
    (X : MarkerMatrix Cell Gene) (S : Finset Gene) (target : Cell)
    (Neighbors : Finset Cell) : Prop :=
  SeparatesFrom X S target Neighbors

/--
If an admissible comparison graph is separated, then each target is separated
from any chosen subset of its admissible neighbors.
-/
theorem admissibleSeparation_gives_target_neighbor_separation
    [DecidableEq Gene] {X : MarkerMatrix Cell Gene} {S : Finset Gene}
    {Global Neighbors : Finset Cell} {Admissible : Cell → Cell → Prop}
    {target : Cell}
    (htarget : target ∈ Global)
    (hneighbors : ∀ n : Cell, n ∈ Neighbors → n ∈ Global ∧ Admissible target n)
    (hsep : SeparatesAdmissibleOn X S Global Admissible) :
    SeparatesTargetNeighbors X S target Neighbors := by
  intro neighbor hneighbor hne
  exact hsep target htarget neighbor (hneighbors neighbor hneighbor).1 hne
    (hneighbors neighbor hneighbor).2

/-- Mean or pseudobulk profile indexed by biological sample or donor. -/
abbrev SampleMeanProfile (Study Sample Partition Group Gene : Type) :=
  Study → Sample → Partition → Group → Gene → ℝ

/-- Pairwise contrast computed within one biological sample or donor. -/
def SamplePairwiseContrast {Study Sample Partition Group Gene : Type}
    (μ : SampleMeanProfile Study Sample Partition Group Gene)
    (study : Study) (sample : Sample) (partition : Partition)
    (target comparison : Group) (gene : Gene) : ℝ :=
  μ study sample partition target gene - μ study sample partition comparison gene

/--
A marker claim supported at the pseudobulk level clears the threshold in every
sample in the chosen sample set.
-/
def ReplicateContrastMarkerGE {Study Sample Partition Group Gene : Type}
    (μ : SampleMeanProfile Study Sample Partition Group Gene)
    (threshold : ℝ) (study : Study) (samples : Finset Sample)
    (partition : Partition) (target comparison : Group) (gene : Gene) : Prop :=
  ∀ sample : Sample, sample ∈ samples →
    threshold ≤ SamplePairwiseContrast μ study sample partition target comparison gene

/--
Replicate-supported marker claims are downward closed in the sample set.
-/
theorem replicateContrastMarkerGE_subset_samples
    {Study Sample Partition Group Gene : Type}
    {μ : SampleMeanProfile Study Sample Partition Group Gene}
    {threshold : ℝ} {study : Study} {LocalSamples GlobalSamples : Finset Sample}
    {partition : Partition} {target comparison : Group} {gene : Gene}
    (hsubset : LocalSamples ⊆ GlobalSamples)
    (hglobal : ReplicateContrastMarkerGE μ threshold study GlobalSamples
      partition target comparison gene) :
    ReplicateContrastMarkerGE μ threshold study LocalSamples
      partition target comparison gene := by
  intro sample hsample
  exact hglobal sample (hsubset hsample)

/--
A scoped marker claim carries the comparison family. Its flat projection keeps
only the target and gene, intentionally discarding the comparison scope.
-/
structure ScopedContrastClaim (Group Gene : Type) where
  target : Group
  comparisons : Finset Group
  gene : Gene

def ScopedContrastClaim.flatProjection {Group Gene : Type}
    (claim : ScopedContrastClaim Group Gene) : Group × Gene :=
  (claim.target, claim.gene)

/--
Flattening scoped marker claims loses comparison-family information: two claims
with the same target and gene but different scopes have the same flat
projection.
-/
theorem flatProjection_eq_of_same_target_gene {Group Gene : Type}
    {claim₁ claim₂ : ScopedContrastClaim Group Gene}
    (htarget : claim₁.target = claim₂.target) (hgene : claim₁.gene = claim₂.gene) :
    claim₁.flatProjection = claim₂.flatProjection := by
  cases claim₁
  cases claim₂
  simp [ScopedContrastClaim.flatProjection] at htarget hgene ⊢
  exact ⟨htarget, hgene⟩

/--
The flat `(target, gene)` projection can identify two distinct scoped marker
claims. In particular, it forgets which comparison family made the claim true.
-/
theorem flatProjection_forgets_comparisons :
    ∃ claim₁ claim₂ : ScopedContrastClaim Bool Bool,
      claim₁.flatProjection = claim₂.flatProjection ∧
        claim₁.comparisons ≠ claim₂.comparisons := by
  refine
    ⟨{ target := true, comparisons := ({false} : Finset Bool), gene := true },
      { target := true, comparisons := (∅ : Finset Bool), gene := true }, ?_⟩
  constructor
  · rfl
  · decide

/--
If a marker panel separates all cell types/profiles, the induced binary
signature map is injective.
-/
theorem signature_injective_of_separates [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {S : Finset Gene} (h : Separates X S) :
    Function.Injective (signature X S) := by
  intro c₁ c₂ hsig
  by_contra hne
  rcases h c₁ c₂ hne with ⟨g, hgS, hdiff⟩
  have hsame :=
    congrArg (fun f : {g // g ∈ S} → Bool => f ⟨g, hgS⟩) hsig
  exact hdiff hsame

/--
Information-theoretic lower bound for binary marker panels.

If `S` separates all cell types/profiles, then the number of cell types/profiles
is at most the number of possible binary signatures on `S`.
-/
theorem card_le_two_pow_of_separates [Fintype Cell] [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} (h : Separates X S) :
    Fintype.card Cell ≤ 2 ^ S.card := by
  have hinj : Function.Injective (signature X S) :=
    signature_injective_of_separates h
  calc
    Fintype.card Cell ≤ Fintype.card ({g // g ∈ S} → Bool) :=
      Fintype.card_le_of_injective (signature X S) hinj
    _ = Fintype.card Bool ^ Fintype.card {g // g ∈ S} := by
      exact Fintype.card_fun
    _ = 2 ^ S.card := by
      simp

/--
Finite-set version of the binary marker-panel information bound. If a marker
panel separates a finite comparison set `Cset`, then the number of profiles in
that comparison set is at most the number of binary signatures available on the
panel.
-/
theorem card_le_two_pow_of_separatesOn [DecidableEq Cell] [DecidableEq Gene]
    {X : MarkerMatrix Cell Gene} {S : Finset Gene} {Cset : Finset Cell}
    (h : SeparatesOn X S Cset) :
    Cset.card ≤ 2 ^ S.card := by
  let Y : MarkerMatrix {c // c ∈ Cset} Gene := fun c g => X c.1 g
  have hsep : Separates Y S := by
    intro c₁ c₂ hne
    have hne_val : c₁.1 ≠ c₂.1 := by
      intro hval
      exact hne (Subtype.ext hval)
    exact h c₁.1 c₁.2 c₂.1 c₂.2 hne_val
  simpa using
    (card_le_two_pow_of_separates
      (Cell := {c // c ∈ Cset}) (Gene := Gene) (X := Y) (S := S) hsep)

/--
Adding markers cannot destroy separation. If `S` already separates all profiles,
then every larger panel `T` also separates them.
-/
theorem separates_mono [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {S T : Finset Gene} (hST : S ⊆ T) (hS : Separates X S) :
    Separates X T := by
  intro c₁ c₂ hne
  rcases hS c₁ c₂ hne with ⟨g, hgS, hdiff⟩
  exact ⟨g, hST hgS, hdiff⟩

/--
Adding markers refines the induced equivalence relation. If two profiles agree
on a larger marker panel, then they agree on every smaller marker panel.
-/
theorem sameOn_antitone [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {S T : Finset Gene} {c₁ c₂ : Cell} (hST : S ⊆ T) :
    SameOn X T c₁ c₂ → SameOn X S c₁ c₂ := by
  intro hT g hgS
  exact hT g (hST hgS)

/--
A minimum separating marker panel is a separating panel with minimum cardinality.
This is the mathematical object approximated by ILP marker-panel selection.
-/
def IsMinimumSeparatingSet [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (S : Finset Gene) : Prop :=
  Separates X S ∧ ∀ T : Finset Gene, Separates X T → S.card ≤ T.card

/--
An essential gene is present in every minimum separating marker panel.
-/
def EssentialGene [DecidableEq Gene] (X : MarkerMatrix Cell Gene) (g : Gene) : Prop :=
  ∀ S : Finset Gene, IsMinimumSeparatingSet X S → g ∈ S

/--
An exchangeable gene is present in at least one, but not every, minimum
separating marker panel.
-/
def ExchangeableGene [DecidableEq Gene] (X : MarkerMatrix Cell Gene) (g : Gene) : Prop :=
  (∃ S : Finset Gene, IsMinimumSeparatingSet X S ∧ g ∈ S) ∧
    ¬ EssentialGene X g

/--
A gene is redundant relative to minimum separation if it is absent from every
minimum separating panel.
-/
def RedundantForMinimumSeparation [DecidableEq Gene] (X : MarkerMatrix Cell Gene)
    (g : Gene) : Prop :=
  ∀ S : Finset Gene, IsMinimumSeparatingSet X S → g ∉ S

/--
An exchangeable gene is not essential by definition: it appears in some minimum
panel but not all of them.
-/
theorem exchangeableGene_not_essential [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {g : Gene} (h : ExchangeableGene X g) :
    ¬ EssentialGene X g :=
  h.2

/--
An exchangeable gene is witnessed by at least one minimum separating panel that
contains it.
-/
theorem exchangeableGene_mem_some_minimum [DecidableEq Gene] {X : MarkerMatrix Cell Gene}
    {g : Gene} (h : ExchangeableGene X g) :
    ∃ S : Finset Gene, IsMinimumSeparatingSet X S ∧ g ∈ S :=
  h.1

/-
Minimum separating sets need not be unique. This two-cell/two-gene example has
two one-gene panels that each separate the cells.
-/
namespace TwoByTwoExample

inductive C where
  | c₀
  | c₁
deriving DecidableEq, Fintype

inductive G where
  | g₀
  | g₁
deriving DecidableEq, Fintype

def X : MarkerMatrix C G
  | C.c₀, G.g₀ => true
  | C.c₀, G.g₁ => false
  | C.c₁, G.g₀ => false
  | C.c₁, G.g₁ => true

theorem g₀_separates : Separates X {G.g₀} := by
  intro a b hne
  fin_cases a <;> fin_cases b
  · exact False.elim (hne rfl)
  · exact ⟨G.g₀, by simp, by decide⟩
  · exact ⟨G.g₀, by simp, by decide⟩
  · exact False.elim (hne rfl)

theorem g₁_separates : Separates X {G.g₁} := by
  intro a b hne
  fin_cases a <;> fin_cases b
  · exact False.elim (hne rfl)
  · exact ⟨G.g₁, by simp, by decide⟩
  · exact ⟨G.g₁, by simp, by decide⟩
  · exact False.elim (hne rfl)

theorem no_empty_panel_separates : ¬ Separates X (∅ : Finset G) := by
  intro h
  rcases h C.c₀ C.c₁ (by decide) with ⟨g, hg, _hdiff⟩
  simp at hg

theorem singleton_minimal (g : G) (hsep : Separates X {g}) :
    IsMinimumSeparatingSet X {g} := by
  constructor
  · exact hsep
  · intro T hT
    have hpos : 0 < T.card := by
      by_contra hnot
      have hzero : T.card = 0 := Nat.eq_zero_of_not_pos hnot
      have hT_empty : T = ∅ := Finset.card_eq_zero.mp hzero
      subst T
      exact no_empty_panel_separates hT
    simpa using Nat.succ_le_of_lt hpos

theorem g₀_minimum : IsMinimumSeparatingSet X {G.g₀} :=
  singleton_minimal G.g₀ g₀_separates

theorem g₁_minimum : IsMinimumSeparatingSet X {G.g₁} :=
  singleton_minimal G.g₁ g₁_separates

theorem minimum_sets_not_unique : {G.g₀} ≠ ({G.g₁} : Finset G) := by
  intro h
  have hg : G.g₀ ∈ ({G.g₁} : Finset G) := by
    have hself : G.g₀ ∈ ({G.g₀} : Finset G) := Finset.mem_singleton_self G.g₀
    rw [h] at hself
    exact hself
  simp at hg

theorem g₀_exchangeable : ExchangeableGene X G.g₀ := by
  constructor
  · exact ⟨{G.g₀}, g₀_minimum, by simp⟩
  · intro hessential
    have hg : G.g₀ ∈ ({G.g₁} : Finset G) := hessential {G.g₁} g₁_minimum
    simp at hg

end TwoByTwoExample

/-!
## Contrast markers require a comparison group

The next example lives at the real-valued contrast level. A single gene can be
a marker for the same target group in one comparison and not a marker for that
same target group in another comparison. This is the formal object behind the
biological examples such as `TRAC` marking T cells against non-T cells but not
distinguishing one T-cell subtype from another.
-/
namespace ContrastComparisonExample

inductive Study where
  | s
deriving DecidableEq, Fintype

inductive Partition where
  | immune
deriving DecidableEq, Fintype

inductive Group where
  | tcell
  | bcell
  | cd4t
deriving DecidableEq, Fintype

inductive MarkerGene where
  | trac
deriving DecidableEq, Fintype

def μ : LocalMeanProfile Study Partition Group MarkerGene
  | Study.s, Partition.immune, Group.tcell, MarkerGene.trac => 10
  | Study.s, Partition.immune, Group.bcell, MarkerGene.trac => 0
  | Study.s, Partition.immune, Group.cd4t, MarkerGene.trac => 10

/--
The same target group and gene have different marker status when the comparison
group changes. Here `trac` separates the target T-cell group from B cells at
threshold 5, but not from a CD4 T-cell subgroup with the same expression level.
-/
theorem marker_status_depends_on_comparison_group :
    PairwiseContrastMarker μ 5 Study.s Partition.immune Group.tcell Group.bcell MarkerGene.trac ∧
      ¬ PairwiseContrastMarker μ 5 Study.s Partition.immune Group.tcell Group.cd4t MarkerGene.trac := by
  constructor
  · norm_num [PairwiseContrastMarker, LocalPairwiseContrast, μ]
  · norm_num [PairwiseContrastMarker, LocalPairwiseContrast, μ]

/--
The same target group and gene also have different marker status when the
one-vs-background comparison changes.
-/
theorem marker_status_depends_on_background :
    BackgroundContrastMarker μ 5 Study.s Partition.immune Group.tcell
        ({Group.bcell} : Finset Group) (fun _ => 1) MarkerGene.trac ∧
      ¬ BackgroundContrastMarker μ 5 Study.s Partition.immune Group.tcell
        ({Group.cd4t} : Finset Group) (fun _ => 1) MarkerGene.trac := by
  constructor
  · norm_num [BackgroundContrastMarker, LocalBackgroundContrast, μ]
  · norm_num [BackgroundContrastMarker, LocalBackgroundContrast, μ]

/--
A restricted comparison family can support a marker claim that fails for a
larger family. This is the contrast-level version of a local marker: `trac`
marks the target T-cell group relative to the restricted `{bcell}` comparison,
but not relative to the broader `{bcell, cd4t}` family.
-/
theorem local_family_marker_not_global_family_marker :
    ContrastFamilyMarker μ 5 Study.s Partition.immune Group.tcell
        ({Group.bcell} : Finset Group) MarkerGene.trac ∧
      ¬ ContrastFamilyMarker μ 5 Study.s Partition.immune Group.tcell
        ({Group.bcell, Group.cd4t} : Finset Group) MarkerGene.trac := by
  constructor
  · intro comparison hcomparison
    simp at hcomparison
    subst comparison
    norm_num [PairwiseContrastMarker, LocalPairwiseContrast, μ]
  · intro hglobal
    have hcd4 := hglobal Group.cd4t (by simp)
    norm_num [PairwiseContrastMarker, LocalPairwiseContrast, μ] at hcd4

end ContrastComparisonExample

namespace PooledBackgroundExample

inductive Study where
  | s
deriving DecidableEq, Fintype

inductive Partition where
  | immune
deriving DecidableEq, Fintype

inductive Group where
  | tcell
  | bcell
  | cd4t
deriving DecidableEq, Fintype

inductive MarkerGene where
  | trac
deriving DecidableEq, Fintype

def μ : LocalMeanProfile Study Partition Group MarkerGene
  | Study.s, Partition.immune, Group.tcell, MarkerGene.trac => 10
  | Study.s, Partition.immune, Group.bcell, MarkerGene.trac => 0
  | Study.s, Partition.immune, Group.cd4t, MarkerGene.trac => 8

/--
A pooled one-vs-background test can pass while one pairwise comparison fails.
With target mean 10, background means 0 and 8, and threshold 5, the
equal-weight pooled contrast is `10 - (0 + 8)/2 = 6 > 5`, yet the pairwise
contrast against the second group is `10 - 8 = 2 < 5`. Pooled one-vs-rest
statistics and the conjunction of pairwise comparisons are therefore not
equivalent marker definitions.
-/
theorem pooled_background_passes_while_pairwise_fails :
    BackgroundContrastMarker μ 5 Study.s Partition.immune Group.tcell
        ({Group.bcell, Group.cd4t} : Finset Group) (fun _ => (1 : ℝ) / 2)
        MarkerGene.trac ∧
      ¬ PairwiseContrastMarker μ 5 Study.s Partition.immune Group.tcell
        Group.cd4t MarkerGene.trac := by
  constructor
  · norm_num [BackgroundContrastMarker, LocalBackgroundContrast, μ,
      Finset.sum_pair (by decide : Group.bcell ≠ Group.cd4t)]
  · norm_num [PairwiseContrastMarker, LocalPairwiseContrast, μ]

end PooledBackgroundExample

/-!
## Adding a comparison cell type can change marker status

The next example makes the local nature of a marker claim explicit. One gene
separates two cell types in a two-row comparison set. After adding a third cell
type with the same binary value as the first, the same gene no longer separates
the enlarged comparison set.
-/
namespace AddingCellTypeExample

inductive C where
  | a
  | b
  | c
deriving DecidableEq, Fintype

inductive G where
  | g
deriving DecidableEq, Fintype

def X : MarkerMatrix C G
  | C.a, G.g => true
  | C.b, G.g => false
  | C.c, G.g => true

def localSet : Finset C := {C.a, C.b}

def withThird : Finset C := {C.a, C.b, C.c}

theorem local_separates : SeparatesOn X {G.g} localSet := by
  intro c₁ hc₁ c₂ hc₂ hne
  refine ⟨G.g, by simp, ?_⟩
  fin_cases c₁ <;> fin_cases c₂ <;> simp [localSet, X] at hc₁ hc₂ hne ⊢

theorem not_withThird_separates : ¬ SeparatesOn X {G.g} withThird := by
  intro h
  rcases h C.a (by simp [withThird]) C.c (by simp [withThird]) (by decide) with
    ⟨gene, _hgene, hdiff⟩
  fin_cases gene
  simp [X] at hdiff

/--
A one-gene marker claim can hold for a local two-cell-type partition but fail
after the comparison set is enlarged with a third cell type.
-/
theorem adding_celltype_can_destroy_marker :
    SeparatesOn X {G.g} localSet ∧ ¬ SeparatesOn X {G.g} withThird := by
  exact ⟨local_separates, not_withThird_separates⟩

end AddingCellTypeExample

/-!
## Local versus global marker separation

The following example formalizes the practical distinction between local marker
claims inside individual papers and global marker claims for atlas building.
Each paper-level comparison set is separable by the same one-gene panel, but the
pooled global comparison set is not separable because profiles from different
papers can have identical marker signatures.
-/
namespace LocalGlobalExample

inductive C where
  | a₀
  | a₁
  | b₀
  | b₁
deriving DecidableEq, Fintype

inductive G where
  | g
deriving DecidableEq, Fintype

def X : MarkerMatrix C G
  | C.a₀, G.g => true
  | C.a₁, G.g => false
  | C.b₀, G.g => true
  | C.b₁, G.g => false

def paperA : Finset C := {C.a₀, C.a₁}

def paperB : Finset C := {C.b₀, C.b₁}

def atlas : Finset C := {C.a₀, C.a₁, C.b₀, C.b₁}

theorem paperA_separates : SeparatesOn X {G.g} paperA := by
  intro c₁ hc₁ c₂ hc₂ hne
  refine ⟨G.g, by simp, ?_⟩
  fin_cases c₁ <;> fin_cases c₂ <;> simp [paperA, X] at hc₁ hc₂ hne ⊢

theorem paperB_separates : SeparatesOn X {G.g} paperB := by
  intro c₁ hc₁ c₂ hc₂ hne
  refine ⟨G.g, by simp, ?_⟩
  fin_cases c₁ <;> fin_cases c₂ <;> simp [paperB, X] at hc₁ hc₂ hne ⊢

theorem not_atlas_separates : ¬ SeparatesOn X {G.g} atlas := by
  intro h
  rcases h C.a₀ (by simp [atlas]) C.b₀ (by simp [atlas]) (by decide) with
    ⟨gene, _hgene, hdiff⟩
  fin_cases gene
  simp [X] at hdiff

/--
Local separation in every paper does not imply global separation after pooling
the paper-level profiles.
-/
theorem local_separation_without_global :
    SeparatesOn X {G.g} paperA ∧ SeparatesOn X {G.g} paperB ∧
      ¬ SeparatesOn X {G.g} atlas := by
  exact ⟨paperA_separates, paperB_separates, not_atlas_separates⟩

end LocalGlobalExample

end MarkerIdentifiability
