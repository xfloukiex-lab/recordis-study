# Recordis — the study record

**Live record:** https://xfloukiex-lab.github.io/recordis-study/

> Atrial fibrillation is classified against a store of the individual patient's own labelled rhythm episodes, with each classification traceable to the episodes that produced it.

By **Alexander Parnell · Vektorgeist · vektorgeist.com/research**

Papers of record: [Comparing Processes as Curves of Distributions (underlying distance)](https://doi.org/10.5281/zenodo.21612829) · [Learning Without Weights (learning method)](https://doi.org/10.5281/zenodo.21612831)

*This file is GENERATED from `manifest.json` by `gen_docs.py`. Do not edit it by hand — a hand-written summary is the first thing to go stale after a retraction, and then the most-read file in the repo is the one that is wrong.*

## Where the record stands

| Status | Count | Meaning |
|---|---:|---|
| Active | 3 | Survives the controls it was tested against. |
| Negative | 3 | Tested and did not hold. |
| **Total** | **6** | |

**3 negative results and 0 retractions are in here on purpose.** A retraction keeps its original wording visible with the reason it was wrong next to it. `check.py` fails the build if a retraction carries no explanation — that would be a deletion, not a retraction.

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

- **[5] Continuous recording with no exclusions: 0.966 accuracy; AF onset detected in the first window of every episode** — rung 3, 2026-08-05  
  Findings 2 and 4 excluded windows spanning a rhythm transition, which are the windows containing episode onset and offset. Scoring every window with no exclusions, mixed windows assigned by majority class, accuracy was 0.966 across nine patients. Transition windows were classified less accurately than pure windows (0.902 against 0.969) without moving the overall figure outside the published range. In 14 AF episodes of at least three windows, the first AF classification occurred in the first window of the episode in every case (median lag 0 windows, 90th percentile 0).
- **[4] Accuracy is limited by store size, not by hyperparameters: 0.983 at 64 stored windows per state** — rung 3, 2026-08-05  
  Two experiments locate the source of the deficit reported in finding 3. A hyperparameter sweep over window length, sub-window length and bin count, tuned on five patients and evaluated on five patients excluded from the sweep, produced no change in held-out accuracy (0.940 for both the sweep-selected and default configurations, while development-set accuracy rose from 0.925 to 0.945). Increasing store size produced 0.935, 0.967 and 0.983 accuracy at 16, 32 and 64 windows per state respectively, still increasing, with the Euclidean control lower at every level.
- **[2] Rhythm-level classification: per-patient AF detection reaches 0.935 at 16 stored windows per state** — rung 3, 2026-08-05  
  Classification of atrial fibrillation from inter-beat interval dynamics, against the same patient's own non-AF rhythm, reached 0.935 accuracy at 16 stored windows per state (chance 0.500). Reconstruction accuracy was 0.89–0.92 at every coverage level tested, in contrast to finding 1 where it did not increase.

### Negative

- **[6] Replication on an independent database: holds for 11 of 12 patients, fails below chance for one** — rung 4, 2026-08-05  
  The finding 5 protocol was repeated without modification on the Long Term AF Database — different patients, different recordings, longer durations, 128 Hz rather than 250 Hz. Mean accuracy across 12 patients was 0.893, below the pre-registered replication threshold of 0.90, and the criterion is recorded as failed. The mean is not representative of the distribution: 11 of the 12 patients scored between 0.660 and 1.000 with a mean of 0.942, and a single patient scored 0.350 — below the 0.500 chance level for a two-class problem, indicating a systematic rather than random failure for that recording. Onset latency replicated without qualification: median 0 windows across the episodes measured.
- **[3] Comparison to published detectors, and to a population reference store, at equal store size** — rung 3, 2026-08-05  
  Neither pre-registered comparison was met. Published interval-based AF detectors report 95–98% accuracy on this database; the untuned method reached 93.5%. With store size held equal, a store composed of the patient's own windows exceeded a store composed of other patients' windows by 2.7 points accuracy and 3.7 points specificity across ten patients, against 10-point thresholds.
- **[1] Single-beat morphology: classification does not reach the pre-registered threshold** — rung 3, 2026-08-05  
  Classification of individual heartbeats by waveform morphology (five rhythm classes, single patient, ECG5000) did not meet its pre-registered criteria. Recognition accuracy increased with the number of stored examples (0.370, 0.428, 0.517, 0.517 for stores of 1, 2, 4 and 8 examples per class; chance 0.200) but plateaued at approximately half the 0.85 threshold. Reconstruction accuracy did not increase across the same range (0.407, 0.450, 0.417, 0.467).

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
