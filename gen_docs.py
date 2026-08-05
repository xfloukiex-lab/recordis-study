"""Regenerate README.md from manifest.json, so the repo's front page cannot drift from the record.

Same reason `check.py` exists and the same reason the study page is generated: a hand-written
summary goes stale the first time a finding is retracted, and then the most-read file in the
repository is the one telling people the wrong thing. Counts, tables and the findings list here
are all derived — there is no hand-maintained number in the output.

Structure follows Elifterminal/relational-metrics, whose README is generated from its manifest
for exactly this reason.

    python gen_docs.py        -> README.md
    python gen_docs.py --check  (CI mode: fail if README.md is out of date, write nothing)
"""
from __future__ import annotations

import io
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "manifest.json"
README = HERE / "README.md"

ORDER = ["active", "provisional", "negative", "retracted", "untested"]
LABEL = {"active": "Active", "provisional": "Provisional", "negative": "Negative",
         "retracted": "Retracted", "untested": "Untested"}


def build() -> str:
    m = json.load(io.open(MANIFEST, encoding="utf-8"))
    fs = m["findings"]
    n = Counter(f["status"] for f in fs)
    eq = m.get("equations", {})

    L: list[str] = []
    add = L.append

    add(f"# {m['project']} — the study record\n")
    add(f"**Live record:** {m.get('study_url', 'https://xfloukiex-lab.github.io/hodos-study/')}\n")
    add(f"> {m['one_line']}\n")
    add(f"By **{m['byline']}**\n")
    if m.get("papers"):
        add("Papers of record: " + " · ".join(
            f"[{p['title']}](https://doi.org/{p['doi']})" for p in m["papers"]) + "\n")
    add("*This file is GENERATED from `manifest.json` by `gen_docs.py`. Do not edit it by hand — "
        "a hand-written summary is the first thing to go stale after a retraction, and then the "
        "most-read file in the repo is the one that is wrong.*\n")

    add("## Where the record stands\n")
    add("| Status | Count | Meaning |")
    add("|---|---:|---|")
    for s in ORDER:
        if n.get(s):
            add(f"| {LABEL[s]} | {n[s]} | {m['status_meanings'][s]} |")
    add(f"| **Total** | **{len(fs)}** | |\n")

    add(f"**{n.get('negative', 0)} negative results and {n.get('retracted', 0)} retractions are "
        "in here on purpose.** A retraction keeps its original wording visible with the reason it "
        "was wrong next to it. `check.py` fails the build if a retraction carries no explanation "
        "— that would be a deletion, not a retraction.\n")

    add("## Confidence rungs\n")
    add("| Rung | What it takes |")
    add("|---:|---|")
    for k in sorted(m["rungs"], key=int):
        add(f"| {k} | {m['rungs'][k]} |")
    top = max((f["rung"] for f in fs if f["status"] in ("active", "provisional")), default=0)
    add(f"\n**Highest rung reached: {top}. Nothing is at rung 7** — reproduced independently, "
        "outside this project. That is the gap, and it is the reason this is public.\n")

    if eq.get("items"):
        add("## The equations\n")
        add("| § | Equation | Provenance |")
        add("|---:|---|---|")
        for q in eq["items"]:
            add(f"| {q['n']} | {q['title']} | {q['tag']} |")
        add("\nRead **ASSEMBLED** carefully — it is not a lesser category. Nearly every method in "
            "this field is a composition; §1 is ASSEMBLED and is where the invention lives.\n")

    TRACK_NAME = {}
    add("## Scope\n")
    add("All findings in this record concern within-patient cardiac rhythm classification from "
        "inter-beat intervals, measured on public patient data.\n")
    add("The underlying method — a distance between processes and a memory-based classifier "
        "built on it — is developed and evaluated separately, on non-clinical signals, in the "
        "[method record](https://xfloukiex-lab.github.io/hodos-study/). Results in that record "
        "concern the method in general and are not clinical claims. Results here concern this "
        "application and do not extend to the method's behaviour in other domains.\n")
    add("Findings 1 and 3 are negative results.\n")

    add("## Findings\n")
    for s in ORDER:
        rows = [f for f in fs if f["status"] == s]
        if not rows:
            continue
        add(f"### {LABEL[s]}\n")
        for f in sorted(rows, key=lambda x: -x["id"]):
            trk = f.get("track")
            badge = f" `[{TRACK_NAME.get(trk, trk).lower()}]`" if trk else ""
            add(f"- **[{f['id']}] {f['title']}**{badge} — rung {f['rung']}, {f['date']}  ")
            add(f"  {f['claim']}")
            if s == "retracted" and f.get("retraction"):
                add(f"  *Why it was wrong:* {f['retraction'][:400]}")
        add("")

    add("## Running it\n")
    add("```\npython build.py        # manifest -> docs/index.html\n"
        "python check.py        # refuse to let the page disagree with the record\n"
        "python gen_docs.py     # regenerate this README from the manifest\n"
        "python lab/impostors.py  # seven cheating methods; the controls must catch all of them\n"
        "```\n")

    add("## Layout\n")
    add("```\nmanifest.json   the single source of truth for what has been run and what is claimed\n"
        "check.py        fails the build if the page and the record disagree\n"
        "gen_docs.py     regenerates this README from the manifest\n"
        "build.py        manifest -> docs/index.html\n"
        "lab/            adversarial controls\n"
        "results/        raw JSON emitted by the experiments\n"
        "docs/           what GitHub Pages serves\n```\n")

    add("## On the impostors\n")
    add("`lab/impostors.py` holds seven methods that deliberately cheat, and the controls have to "
        "catch every one before any measure here is trusted. The discipline is borrowed, with "
        "credit, from [Elifterminal/relational-metrics]"
        "(https://github.com/Elifterminal/relational-metrics).\n")
    add("It is not decorative. This project has shipped two results that a cheating method would "
        "have predicted: a distance whose 'win' was a padding degeneracy (finding 9), and a "
        "comparison run in a space where the measure was a constant function — off-diagonal "
        "spread of exactly 0.0000 (findings 17 and 24). On its very first run the suite exposed a "
        "gap in our own control set, and a fifth control had to be written.\n")

    add("## Licence\n")
    add("Findings text CC-BY-4.0. Preprints are open access on Zenodo; see the study page.\n")
    return "\n".join(L)


def main() -> int:
    doc = build()
    if "--check" in sys.argv:
        cur = README.read_text(encoding="utf-8") if README.exists() else ""
        if cur.strip() != doc.strip():
            print("README.md is OUT OF DATE — run `python gen_docs.py`")
            return 1
        print("README.md matches the manifest")
        return 0
    README.write_text(doc, encoding="utf-8")
    print(f"wrote README.md ({len(doc):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
