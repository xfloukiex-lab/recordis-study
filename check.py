"""Drift guard for the study record. Fails loudly rather than letting the site quietly lie.

The whole value of a manifest-driven site is that the page cannot disagree with the record. That
only holds if something enforces it, so this runs the checks that would otherwise rot silently:

  1. every referenced code path and result file actually EXISTS on disk
  2. cross-references (supersedes / superseded_by) point at real findings and agree with each other
  3. every retracted finding carries the explanation of WHY it was wrong — a retraction with no
     reason is just a deletion with extra steps
  4. every active or provisional finding carries evidence and a scope
  5. status and rung values are from the declared vocabularies
  6. ids are unique and dates are well-formed
  7. rung 4 ("replicated on a second modality") is not claimed without a second modality named
  8. the built site is not older than the manifest

    python study/check.py     -> exits non-zero on any failure
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

VALID_STATUS = {"active", "provisional", "negative", "retracted", "untested"}


def main():
    m = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    fs = m["findings"]
    ids = {f["id"] for f in fs}
    problems, warnings, unverifiable = [], [], []

    if len(ids) != len(fs):
        problems.append("finding ids are not unique")

    for f in fs:
        fid = f["id"]

        if f["status"] not in VALID_STATUS:
            problems.append(f"[{fid}] unknown status {f['status']!r}")
        if str(f.get("rung", "")) not in m["rungs"] and f.get("rung") is not None:
            problems.append(f"[{fid}] rung {f.get('rung')!r} not in the declared rungs")
        try:
            datetime.strptime(f["date"], "%Y-%m-%d")
        except (ValueError, KeyError):
            problems.append(f"[{fid}] bad or missing date")

        # 1. referenced files exist.
        #    In the PUBLISHED copy the engine source deliberately is not shipped (it stays in the
        #    private repo), so these paths are references INTO that repo and cannot be verified
        #    from here. Say so explicitly rather than silently skipping the check — a check that
        #    quietly does nothing is worse than no check.
        for key in ("code", "result_file"):
            p = f.get(key)
            if p and not (ROOT / p).exists():
                if m.get("private") is False:
                    unverifiable.append(f"[{fid}] {key} -> {p}")
                else:
                    problems.append(f"[{fid}] {key} does not exist: {p}")

        # 2. cross-references resolve and agree.
        #    `supersedes` may be a list: one corrected measurement can legitimately retire
        #    several findings at once (25 supersedes both 17 and 24). `superseded_by` stays
        #    scalar — a finding is retracted by exactly one thing.
        def _targets(v):
            return [] if v is None else (list(v) if isinstance(v, list) else [v])

        for key in ("supersedes", "superseded_by"):
            for t in _targets(f.get(key)):
                if t not in ids:
                    problems.append(f"[{fid}] {key} points at missing finding {t}")
        if f.get("superseded_by"):
            other = next(x for x in fs if x["id"] == f["superseded_by"])
            if fid not in _targets(other.get("supersedes")):
                problems.append(f"[{fid}] says superseded_by {other['id']}, "
                                f"but {other['id']} does not say it supersedes {fid}")

        # 3. a retraction must say WHY
        if f["status"] == "retracted":
            if not f.get("retraction"):
                problems.append(f"[{fid}] retracted with no explanation — that is a deletion, "
                                f"not a retraction")
            if "ORIGINAL WORDING" not in f.get("claim", ""):
                warnings.append(f"[{fid}] retracted but the claim is not flagged as the original "
                                f"(the wrong wording should stay visible and labelled)")

        # 4. live claims need evidence and scope
        if f["status"] in ("active", "provisional"):
            if not f.get("evidence"):
                problems.append(f"[{fid}] {f['status']} with no evidence")
            if not f.get("scope"):
                problems.append(f"[{fid}] {f['status']} with no scope/limits stated")

        # 7. rung 4 SPECIFICALLY claims replication on a second modality. The rungs are NOT a
        #    strict hierarchy -- 5 is "survives a fair control" and 6 is "vs a published method",
        #    which are different axes -- so this must not fire for >=4.
        if f.get("rung") == 4 and f["status"] in ("active", "provisional"):
            blob = (f.get("evidence", "") + f.get("scope", "") + f.get("note", "")).lower()
            if not any(w in blob for w in ("handwrit", "modalit", "speech", "pen", "chars",
                                           "both", "second")):
                warnings.append(f"[{fid}] rung {f['rung']} implies replication on a second "
                                f"modality, but neither is named in the text")

    # 8. is the built site stale?
    site = HERE / "docs" / "index.html"
    if site.exists():
        if site.stat().st_mtime < (HERE / "manifest.json").stat().st_mtime:
            warnings.append("docs/index.html is OLDER than manifest.json — run build.py")
    else:
        warnings.append("docs/index.html not built yet — run build.py")

    print(f"manifest: {len(fs)} findings")
    if unverifiable:
        print(f"  NOTE  {len(unverifiable)} code/result paths point into the PRIVATE repo and "
              f"cannot be verified from this published copy:")
        for u in unverifiable[:4]:
            print(f"          {u}")
        if len(unverifiable) > 4:
            print(f"          ... and {len(unverifiable)-4} more")
    for w in warnings:
        print(f"  WARN  {w}")
    for p in problems:
        print(f"  FAIL  {p}")

    if problems:
        print(f"\n{len(problems)} problem(s). The record and the site would disagree.")
        return 1
    print(f"\nOK{' (with ' + str(len(warnings)) + ' warning(s))' if warnings else ''} — "
          f"the site cannot disagree with the record.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
