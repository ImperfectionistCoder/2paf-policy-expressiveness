# 2PAF revision code (IJIES paper no. 20266199)

Code and data supporting the revised manuscript. Built in October 2026 for the revision.

## Contents

- `scoring/weights_and_sensitivity.py`
  Category weights from the 13 coded studies (Table 6, Table 7), policy scores (Table 9),
  and the sensitivity analysis (Section 5.5, Table 10): equal weights, leave-one-study-out,
  bootstrap (10,000 resamples, seed 42) and threshold variation. Needs only numpy.
- `opp115/`
  Category detection (Algorithm 1, lines 3 to 8) and its evaluation on OPP-115 (Section 5.6, Table 11).
  - `pipeline.py`, `keywords.py`: baseline detection, keywords written from the category definitions.
  - `pipeline_v2.py`, `keywords_v2.json`: refined detection, keywords selected on the 75 development policies.
  - `common.py`: data loading, ground truth (category present in a segment when at least 2 of 3 annotators assign it),
    fixed development/test split (seed 2026), evaluation.
  - `kwstats.py`, `select.py`: keyword selection on the development set only.
  - `evaluate.py`: baseline evaluation on all 115 policies.
  - `coverage.py`: per-policy category coverage in OPP-115.
  - `test_ids.txt`: the 40 held-out test policies. `test_results.txt`: output reported in Table 11.
- `policies/GlucoseInsights_privacy_policy_reconstructed.md`
  Synthetic policy for the proof-of-concept application, reconstructed for the revision
  (the original synthetic text was not preserved), with its category labels.

## Data

OPP-115 is not included. Download it from https://usableprivacy.org/data (OPP-115_v1_0.zip),
unzip it, and point `OPP115_DIR` to the `OPP-115` folder.

## Running

    pip install -r requirements.txt
    python scoring/weights_and_sensitivity.py

    cd opp115
    export OPP115_DIR=/path/to/OPP-115
    python coverage.py          # per-policy coverage
    python kwstats.py           # lemmatize development segments (cache)
    python select.py            # select refined keywords on the development set
    python -c "from common import *; import pipeline, pipeline_v2; d=load_all(); dev,test=split(d); evaluate(test,pipeline.detect); evaluate(test,pipeline_v2.detect)"

Running `select.py` again regenerates `keywords_v2.json`; the version included is the one used for Table 11.
