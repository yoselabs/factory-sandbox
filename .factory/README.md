# .factory

**This workspace's queue. Machine-written. Do not edit by hand.**

Under K decision D033 each workspace's queue lives inside that workspace's own repository, so an
item in this directory *is* this repository's item and no other workspace can see it or pay for it.
D034 keeps the credential, the schedule and the transcripts in the private runner and leaves
everything below here local. A turn commits its work and its bookkeeping in the same commit.

## The shape, and what fixes each path

Every name here is a constant in `yoselabs/yosefactory`'s `src/yosefactory/runtime/turn.py`, read
relative to the queue root (`Places.nested`, whose `queue_subdir` defaults to `.factory`). They are
not conventions this file is free to change.

```
.factory/
  backlog/items/*.jsonl   ITEMS      one work item, one file, one JSON event per line
  questions/*.jsonl       QUESTIONS  a blocked turn's question, resolved by an answer event
  ledger/runs/            RUNS       one record per turn: <slug>.start, then <slug>.json
  ledger/spend.jsonl                 one row per model invocation, joined to a run by run_id
```

The item format is specified in `yosefactory` and nowhere else — `protocol/backlog.py` for the event
table the fold enforces. A second copy of it is a second thing to be wrong, so there is none here.

Two properties that decide how anything here may be touched:

- **Append-only.** Nothing is edited, reordered or deleted. An item is closed by appending the event
  that closes it.
- **The state is the fold.** `state`, `lease`, `awaiting` and the frame are replayed from an item's
  own events. Nothing stores them.

## How work gets in

**Open a GitHub issue on this repository.** That is the whole intake path: the runner ingests new
issues into items here. Hand-writing a file in `backlog/items/` bypasses ingest, is picked up by the
next turn as if a human had never been involved, and spends real quota on it.

An empty `backlog/items/` is the normal state and is not a fault. The pre-flight check globs it,
finds nothing, reports `ready=false` and skips the run without paying for anything.
