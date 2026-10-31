# 2PAF source code 

Code and data supporting the paper titled "A Privacy-by-Design Framework for Assessing Privacy Policy Expressiveness in Smart Healthcare Systems"

## Contents

- `scoring/weights_and_sensitivity.py`
  Category weights from the 13 coded studies (Table 6, Table 7), policy scores (Table 9),
  and the sensitivity analysis (Section 5.5, Table 10): equal weights, leave-one-study-out,
  bootstrap (10,000 resamples, seed 42) and threshold variation. Needs only numpy.
- `opp115/`
  Category detection (Algorithm 1, lines 3 to 8) and its evaluation on OPP-115 (Section 5.6, Table 11).
  - `textproc.py`: cleaning, tokenization, stop-word removal and lemmatization (spaCy).
  - `detect.py`, `keywords.json`: category detection with the keywords reported in Section 5.6.
  - `common.py`: data loading, ground truth (a category is present in a segment when at least
    2 of 3 annotators assign it), fixed development/test split (seed 2026), evaluation.
  - `kwstats.py`, `select_keywords.py`: keyword selection on the 75 development policies only.
    The starting keywords written from the category definitions are listed in `select_keywords.py`.
  - `evaluate_test.py`: evaluation on the 40 held-out test policies (Table 11).
  - `coverage.py`: per-policy category coverage in OPP-115.
  - `test_ids.txt`: the 40 test policies. `test_results.txt`: output reported in Table 11.
- `conflict/ahp_example.py`
  AHP computation for the worked example in Section 5.7 (Table 12). Criteria priorities from
  Sadki and El Bakkali [29]; pairwise judgments between the patient preference and the policy are
  the authors' assumptions and are listed in the script.
- `policies/GlucoseInsights_privacy_policy_reconstructed.md`
  Synthetic policy for the proof-of-concept application, with its category labels.
- `review/mapping_protocol.md`, `review/table6_evidence.csv`
  Inclusion criteria and mapping rules for the literature review, and the 13-study matrix (Table 6)
  with the supporting location in each study for every mark.
- `compliance/`
  GDPR transparency compliance check (Section 4.3.3, Table 8; results in Section 5.7, Table 13).
  - `annotation_guide.md`: the 14 requirements, labeling rules and applicability rules.
  - `policies.csv`: the policies, how they were selected (query, position, date) and their links.
  - `labels_annotator_A.csv`, `labels_annotator_B.csv`: the two annotators' labels. Annotator A reviewed
    draft labels prepared with the help of a language model; annotator B labeled from scratch.
  - `ground_truth.csv`: labels after resolving the disagreements.
  - `agreement.py`: computes the agreement (Cohen's kappa) and the result per policy (`python compliance/agreement.py`).
- `opp115/weights_comparison.py`: weighted vs equal-weight scores on the 115 OPP-115 policies (Section 5.6).

## Data

OPP-115 is not included. Download it from https://usableprivacy.org/data (OPP-115_v1_0.zip),
unzip it, and point `OPP115_DIR` to the `OPP-115` folder.

## Running

    pip install -r requirements.txt
    python scoring/weights_and_sensitivity.py
    python conflict/ahp_example.py

    cd opp115
    export OPP115_DIR=/path/to/OPP-115      # PowerShell: $env:OPP115_DIR="C:\path\to\OPP-115"
    python coverage.py                      # per-policy coverage
    python evaluate_test.py                 # Table 11

To regenerate the keywords from the development set:

    python kwstats.py
    python select_keywords.py               # rewrites keywords.json (same result as included)


