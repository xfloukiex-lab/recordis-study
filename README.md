# Recordis — the study record

**Live record:** https://xfloukiex-lab.github.io/recordis-study/

> Atrial fibrillation is classified against a store of the individual patient's own labelled rhythm episodes, with each classification traceable to the episodes that produced it.

By **Alexander Parnell · Vektorgeist · vektorgeist.com/research**

Papers of record: [Comparing Processes as Curves of Distributions (underlying distance)](https://doi.org/10.5281/zenodo.21612829) · [Learning Without Weights (learning method)](https://doi.org/10.5281/zenodo.21612831)

*This file is GENERATED from `manifest.json` by `gen_docs.py`. Do not edit it by hand — a hand-written summary is the first thing to go stale after a retraction, and then the most-read file in the repo is the one that is wrong.*

## Where the record stands

| Status | Count | Meaning |
|---|---:|---|
| Active | 5 | Survives the controls it was tested against. |
| Negative | 3 | Tested and did not hold. |
| Retracted | 1 | Subsequently refuted by our own measurement; original wording retained. |
| **Total** | **9** | |

**3 negative results and 1 retractions are in here on purpose.** A retraction keeps its original wording visible with the reason it was wrong next to it. `check.py` fails the build if a retraction carries no explanation — that would be a deletion, not a retraction.

## Confidence rungs

| Rung | What it takes |
|---:|---|
| 1 | reasoned, unmeasured |
| 2 | measured once, synthetic data |
| 3 | measured on real patient data, single database |
| 4 | replicated on a second, independent patient database |
| 5 | prospective — data recorded after the method was fixed |
| 6 | head-to-head against a deployed clinical device on the same recordings |
| 7 | independently reproduced outside this project |

**Highest rung reached: 3. Nothing is at rung 7** — reproduced independently, outside this project. That is the gap, and it is the reason this is public.

## The equations

| § | Equation | Provenance |
|---:|---|---|
| 1 | Rhythm representation | APPLICATION-SPECIFIC — representation choice, not new mathematics |

Read **ASSEMBLED** carefully — it is not a lesser category. Nearly every method in this field is a composition; §1 is ASSEMBLED and is where the invention lives.

## Scope

All findings in this record concern within-patient cardiac rhythm classification from inter-beat intervals, measured on public patient data.

The underlying method — a distance between processes and a memory-based classifier built on it — is developed and evaluated separately, on non-clinical signals, in the [method record](https://xfloukiex-lab.github.io/hodos-study/). Results in that record concern the method in general and are not clinical claims. Results here concern this application and do not extend to the method's behaviour in other domains.

Findings 1 and 3 are negative results.

## Findings

### Active

- **[9] The failures are physiological, not algorithmic: in those patients the non-AF rhythm is itself irregular** — rung 3, 2026-08-05  
  The patients on which classification fails are those whose two rhythm states do not differ in beat-to-beat variability. Median RMSSD for the non-AF and AF states, and their ratio, across the three lowest- and three highest-scoring patients of finding 7: patient 103, 282 ms non-AF against 109 ms AF (ratio 0.39, score 0.510); patient 11, 240 against 213 (0.89, 0.440); patient 10, 132 against 165 (1.25, 0.560); patient 110, 64 against 186 (2.89, 0.990); patient 00, 15 against 95 (6.50, 1.000); patient 102, 13 against 166 (12.42, 1.000). Every patient with a ratio above 2.8 scored at or above 0.990, and every patient below 1.3 scored at or below 0.560, with no overlap between the groups.
- **[8] Diagnosis of the worst-performing patient: the representation does not separate that patient's two rhythms** — rung 3, 2026-08-05  
  For the patient scoring lowest in finding 7, the representation does not distinguish the two rhythm states at all. Mean distance between windows of opposite class is SMALLER than between windows of the same class (22.64 against 23.34, separation −0.70). A classifier retrieving by that distance is therefore reading noise for this patient, and its output is not merely unreliable but uninformative. Two candidate explanations are excluded: the store and query sets were class-balanced by construction, and accuracy differs little between queries near and far in time from their nearest stored window (0.380 against 0.320), so neither class imbalance nor within-recording drift accounts for it.
- **[5] Continuous recording with no exclusions: 0.966 accuracy; AF onset detected in the first window of every episode** — rung 3, 2026-08-05  
  Findings 2 and 4 excluded windows spanning a rhythm transition, which are the windows containing episode onset and offset. Scoring every window with no exclusions, mixed windows assigned by majority class, accuracy was 0.966 across nine patients. Transition windows were classified less accurately than pure windows (0.902 against 0.969) without moving the overall figure outside the published range. In 14 AF episodes of at least three windows, the first AF classification occurred in the first window of the episode in every case (median lag 0 windows, 90th percentile 0).
- **[4] Accuracy is limited by store size, not by hyperparameters: 0.983 at 64 stored windows per state** — rung 3, 2026-08-05  
  Two experiments locate the source of the deficit reported in finding 3. A hyperparameter sweep over window length, sub-window length and bin count, tuned on five patients and evaluated on five patients excluded from the sweep, produced no change in held-out accuracy (0.940 for both the sweep-selected and default configurations, while development-set accuracy rose from 0.925 to 0.945). Increasing store size produced 0.935, 0.967 and 0.983 accuracy at 16, 32 and 64 windows per state respectively, still increasing, with the Euclidean control lower at every level.
- **[2] Rhythm-level classification: per-patient AF detection reaches 0.935 at 16 stored windows per state** — rung 3, 2026-08-05  
  Classification of atrial fibrillation from inter-beat interval dynamics, against the same patient's own non-AF rhythm, reached 0.935 accuracy at 16 stored windows per state (chance 0.500). Reconstruction accuracy was 0.89–0.92 at every coverage level tested, in contrast to finding 1 where it did not increase.

### Negative

- **[7] Replication, restated with balanced query sets: 0.820 mean balanced accuracy, below the first database** — rung 4, 2026-08-05  
  Repeating the replication with class-balanced query sets, correcting the defect that retracted finding 6: mean balanced accuracy across the same 12 patients is 0.820, against a pre-registered replication threshold of 0.90 and against 0.966 on the first database. The criterion fails, and the corrected figure is lower than the flawed one it replaces. Per-patient balanced accuracy: 1.000, 1.000, 0.990, 0.980, 0.950, 0.920, 0.890, 0.880, 0.720, 0.560, 0.510, 0.440. Onset latency replicates without qualification: median 0 windows over 14 episodes.
- **[3] Comparison to published detectors, and to a population reference store, at equal store size** — rung 3, 2026-08-05  
  Neither pre-registered comparison was met. Published interval-based AF detectors report 95–98% accuracy on this database; the untuned method reached 93.5%. With store size held equal, a store composed of the patient's own windows exceeded a store composed of other patients' windows by 2.7 points accuracy and 3.7 points specificity across ten patients, against 10-point thresholds.
- **[1] Single-beat morphology: classification does not reach the pre-registered threshold** — rung 3, 2026-08-05  
  Classification of individual heartbeats by waveform morphology (five rhythm classes, single patient, ECG5000) did not meet its pre-registered criteria. Recognition accuracy increased with the number of stored examples (0.370, 0.428, 0.517, 0.517 for stores of 1, 2, 4 and 8 examples per class; chance 0.200) but plateaued at approximately half the 0.85 threshold. Reconstruction accuracy did not increase across the same range (0.407, 0.450, 0.417, 0.467).

### Retracted

- **[6] Replication on an independent database: holds for 11 of 12 patients, fails below chance for one** — rung 4, 2026-08-05  
  The finding 5 protocol was repeated without modification on the Long Term AF Database — different patients, different recordings, longer durations, 128 Hz rather than 250 Hz. Mean accuracy across 12 patients was 0.893, below the pre-registered replication threshold of 0.90, and the criterion is recorded as failed. The mean is not representative of the distribution: 11 of the 12 patients scored between 0.660 and 1.000 with a mean of 0.942, and a single patient scored 0.350 — below the 0.500 chance level for a two-class problem, indicating a systematic rather than random failure for that recording. Onset latency replicated without qualification: median 0 windows across the episodes measured.
  *Why it was wrong:* The per-patient figures in this finding are not accuracy. The query sets were taken in recording order, and this database contains long uninterrupted rhythm blocks, so for most patients every queried window carried the same label. A subsequent audit of both databases under the published protocol found single-class query sets for 42 of 56 evaluable patients here — and, separately, for 0 of 9 patien

## Running it

```
python build.py        # manifest -> docs/index.html
python check.py        # refuse to let the page disagree with the record
python gen_docs.py     # regenerate this README from the manifest
python lab/impostors.py  # seven cheating methods; the controls must catch all of them
```

## Layout

```
manifest.json   the single source of truth for what has been run and what is claimed
check.py        fails the build if the page and the record disagree
gen_docs.py     regenerates this README from the manifest
build.py        manifest -> docs/index.html
lab/            adversarial controls
results/        raw JSON emitted by the experiments
docs/           what GitHub Pages serves
```

## On the impostors

`lab/impostors.py` holds seven methods that deliberately cheat, and the controls have to catch every one before any measure here is trusted. The discipline is borrowed, with credit, from [Elifterminal/relational-metrics](https://github.com/Elifterminal/relational-metrics).

It is not decorative. This project has shipped two results that a cheating method would have predicted: a distance whose 'win' was a padding degeneracy (finding 9), and a comparison run in a space where the measure was a constant function — off-diagonal spread of exactly 0.0000 (findings 17 and 24). On its very first run the suite exposed a gap in our own control set, and a fifth control had to be written.

## Licence

Findings text CC-BY-4.0. Preprints are open access on Zenodo; see the study page.
