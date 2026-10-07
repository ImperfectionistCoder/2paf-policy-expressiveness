# Codebook for the literature review (Section 4.2, Table 6)

## Inclusion criteria

A study was included if it
1. was published in a peer-reviewed journal or conference indexed in Scopus,
2. defined, extracted or evaluated the elements that a privacy policy should contain, and
3. was available in full text for coding.

Thirteen studies met these criteria. They were searched in MDPI, IEEE Xplore, PubMed,
ScienceDirect and the ACM Digital Library (publications from 2020 to 2026), with further
studies added while reading the retrieved papers.

## General coding rule

A category is marked as present (1) for a study when the study treats it as an element of
privacy policy content in at least one of the following:

- (a) its own taxonomy, annotation scheme, or list of policy elements;
- (b) the criteria or features it uses to evaluate, score, or classify policies;
- (c) its reported results, where the category is measured or analyzed.

A mention only in the introduction or related work is not counted. When a study covers only
part of a category, it is marked present if the part it covers matches the definition below.

## Categories

| Category | Present when the study treats as policy content... | OPP-115 equivalent |
|---|---|---|
| Data Collection | what personal data is collected, or the purposes of collection and use | First Party Collection/Use |
| Data Retention | how long data is stored, deletion schedules, or storage duration | Data Retention |
| Data Sharing | disclosure of data to third parties, the recipients, or the purposes of sharing | Third Party Sharing/Collection |
| Owner Access | the user's ability to access, correct, export, or delete their data | User Access, Edit and Deletion |
| Owner Control | the user's choices over collection or use (consent, opt-in/opt-out, settings) | User Choice/Control |
| Data Security | measures that protect data (encryption, access control, breach handling) | Data Security |
| Regulatory Conformity | the laws, regulations or certification schemes a service states it follows, or disclosures for specific jurisdictions or audiences | No direct equivalent; partly International and Specific Audiences |

Studies that use the OPP-115 scheme are coded present for Regulatory Conformity through its
International and Specific Audiences category.

## Evidence record

For each mark, the supporting section, table, figure or appendix of the study is recorded in
`table6_evidence.csv`. Marks noted as "borderline" were coded by applying the rule above to a
case that only partly matches the category definition.

## Weights

The weight of a category is its number of present marks divided by the total number of present
marks in the matrix (73). See `scoring/weights_and_sensitivity.py`.
