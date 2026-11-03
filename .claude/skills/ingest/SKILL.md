---
name: ingest
description: Ingest new sources from raw/inbox into the wiki. Use when the user says ingest, clip, process inbox, or after files appear in raw/inbox.
---
1. List files in raw/inbox/ that have no page in wiki/sources/ yet.
2. For each file, call the scout subagent: summary page + candidate pages.
3. Run `python scripts/route.py --dedupe <summary>`; skip exact duplicates.
4. Call the librarian subagent with the summary and the source path.
5. Show me: pages created, pages updated, conflicts found. Max 15 edits per source.