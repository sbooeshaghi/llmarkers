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
