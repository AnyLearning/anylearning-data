#!/usr/bin/env python3
"""Rebuild the small, redistribution-cleared structured dataset mirrors.

Inputs are fixed upstream URLs.  Outputs are normalized UTF-8 CSV files plus a
catalog whose SHA-256 values are used both for publishing and release checks.
Run with pandas and xlrd installed; no credentials are required.
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import pathlib
import urllib.request
import zipfile

import pandas as pd

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "v1"
USER_AGENT = {"User-Agent": "AnyLearning dataset builder/1"}


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers=USER_AGENT)
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def bank_marketing() -> pathlib.Path:
    outer = zipfile.ZipFile(io.BytesIO(download("https://archive.ics.uci.edu/static/public/222/bank+marketing.zip")))
    inner = zipfile.ZipFile(io.BytesIO(outer.read("bank.zip")))
    source = io.TextIOWrapper(inner.open("bank-full.csv"), encoding="utf-8")
    rows = csv.DictReader(source, delimiter=";")
    destination = OUT / "bank-marketing.csv"
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows.fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return destination


def concrete_strength() -> pathlib.Path:
    archive = zipfile.ZipFile(io.BytesIO(download("https://archive.ics.uci.edu/static/public/165/concrete+compressive+strength.zip")))
    frame = pd.read_excel(io.BytesIO(archive.read("Concrete_Data.xls")), engine="xlrd")
    frame.columns = [
        "Cement",
        "Blast Furnace Slag",
        "Fly Ash",
        "Water",
        "Superplasticizer",
        "Coarse Aggregate",
        "Fine Aggregate",
        "Age",
        "Concrete compressive strength",
    ]
    destination = OUT / "concrete-strength.csv"
    frame.to_csv(destination, index=False)
    return destination


def banking77() -> pathlib.Path:
    sources = [
        ("train", "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv"),
        ("test", "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/test.csv"),
    ]
    destination = OUT / "banking77.csv"
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["text", "intent", "source_split"])
        writer.writeheader()
        for split, url in sources:
            rows = csv.DictReader(io.StringIO(download(url).decode("utf-8")))
            for row in rows:
                writer.writerow({"text": row["text"], "intent": row["category"], "source_split": split})
    return destination


def truthfulqa() -> pathlib.Path:
    source = csv.DictReader(
        io.StringIO(
            download(
                "https://raw.githubusercontent.com/sylinrl/TruthfulQA/main/TruthfulQA.csv"
            ).decode("utf-8")
        )
    )
    destination = OUT / "truthfulqa-evaluation.csv"
    fields = [
        "question",
        "candidate_response",
        "reference_answer",
        "category",
        "question_type",
        "source",
    ]
    with destination.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in source:
            writer.writerow(
                {
                    "question": row["Question"],
                    # The benchmark authors supply this as a plausible *wrong*
                    # answer.  Naming it candidate_response avoids claiming it
                    # came from a model; it is useful for showing why lexical
                    # similarity alone is not a truthfulness judge.
                    "candidate_response": row["Best Incorrect Answer"],
                    "reference_answer": row["Best Answer"],
                    "category": row["Category"],
                    "question_type": row["Type"],
                    "source": row["Source"],
                }
            )
    return destination


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def row_count(path: pathlib.Path) -> int:
    with path.open(encoding="utf-8", newline="") as stream:
        return sum(1 for _ in csv.reader(stream)) - 1


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = [bank_marketing(), concrete_strength(), banking77(), truthfulqa()]
    entries = []
    base = {
        "bank-marketing.csv": {
            "slug": "bank-marketing",
            "name": "UCI Bank Marketing",
            "description": "45,211 real bank marketing calls with mixed numeric and categorical columns; predict term-deposit subscription.",
            "task": "classification",
            "target": "y",
            "license": "CC BY 4.0",
            "source_url": "https://archive.ics.uci.edu/dataset/222/bank+marketing",
            "citation": "Moro, Rita & Cortez (2014), doi:10.24432/C5K306",
        },
        "concrete-strength.csv": {
            "slug": "concrete-strength",
            "name": "UCI Concrete Compressive Strength",
            "description": "1,030 concrete mixes with eight measured inputs and compressive strength in MPa.",
            "task": "regression",
            "target": "Concrete compressive strength",
            "license": "CC BY 4.0",
            "source_url": "https://archive.ics.uci.edu/dataset/165/concrete+compressive+strength",
            "citation": "Yeh (1998), doi:10.24432/C5PK67",
        },
        "banking77.csv": {
            "slug": "banking77",
            "name": "Banking77 customer-support intents",
            "description": "13,083 online banking questions labelled with 77 fine-grained intents.",
            "task": "text_classification",
            "target": "intent",
            "text_column": "text",
            "license": "CC BY 4.0",
            "source_url": "https://github.com/PolyAI-LDN/task-specific-datasets/tree/master/banking_data",
            "citation": "Casanueva et al. (2020), arXiv:2003.04807",
        },
        "truthfulqa-evaluation.csv": {
            "slug": "truthfulqa-evaluation",
            "name": "TruthfulQA response evaluation",
            "description": "790 adversarial questions with reference answers and plausible incorrect candidate responses for testing response evaluation.",
            "task": "llm_evaluation",
            "prompt_column": "question",
            "response_column": "candidate_response",
            "reference_column": "reference_answer",
            "license": "Apache 2.0",
            "source_url": "https://github.com/sylinrl/TruthfulQA",
            "citation": "Lin, Hilton & Evans (2022), doi:10.18653/v1/2022.acl-long.229",
        },
    }
    for path in files:
        entries.append(
            {
                **base[path.name],
                "filename": path.name,
                "rows": row_count(path),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "url": f"https://cdn.anylearning.nrl.ai/datasets/structured/v1/{path.name}",
            }
        )
    (ROOT / "catalog-v1.json").write_text(
        json.dumps({"version": 1, "datasets": entries}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for entry in entries:
        print(f"{entry['filename']}: {entry['rows']} rows, {entry['sha256']}")


if __name__ == "__main__":
    main()
