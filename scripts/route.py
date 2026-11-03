#!/usr/bin/env python3
# scripts/route.py "<question>"       ->  prints "sonnet" or "opus"
# scripts/route.py --dedupe <summary> ->  prints "duplicate" or "new"
import sys
from pathlib import Path
from typesafe_sdk import Choice, Noul, TypeSafeClient

jev = TypeSafeClient(model="jev-1.13.0")
index = Path("wiki/index.md").read_text()[-40_000:]
if sys.argv[1] == "--dedupe":
    summary = Path(sys.argv[2]).read_text()[:20_000]
    r = jev.system_one(
        state={"summary": summary, "index": index},
        questions={"dup": Noul(
            instructions="Does `index` already list a page for the same source as `summary`?")},
    )
    print("duplicate" if r.answers["dup"].noul >= 0.9 else "new")
    sys.exit(0)
question = sys.argv[1]
r = jev.system_one(
    state={"question": question, "index": index},
    questions={"depth": Choice(
        instructions="How much work does answering `question` from this wiki take?",
        criteria={
            "lookup": "The answer sits on one or two pages listed in `index`",
            "synthesis": "It needs 4+ pages, a comparison or a new conclusion",
            "other": "None of the above fits",
        })},
)
a = r.answers["depth"]
print("sonnet" if a.choice == "lookup" and a.confidence >= 0.85 else "opus")