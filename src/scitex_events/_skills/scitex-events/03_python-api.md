---
description: |
  [TOPIC] Python API
  [DETAILS] Public Python API of scitex-events — exported functions, signatures,
  return types, and minimal usage examples per function.
tags: [scitex-events-python-api]
---

# Python API

```python
from scitex_events import emit, latest, history, list_types, get_type_info
```

## emit(event_type, project, status="success", payload=None, source="local") -> Event

Emit an event to the local state file and history log.

```python
ev.emit("build_result", project="my-paper", status="failure",
        payload={"doc_type": "latex", "errors": ["missing.bib"]})
```

Returns an `Event` dataclass instance.

## latest(event_type=None) -> dict | None

Read the latest event of a given type, or the most recent across all types.

```python
last = ev.latest("test_complete")
# -> {"type": "test_complete", "project": "figrecipe", "status": "success", ...}
```

Returns `None` if no events exist.

## history(limit=20) -> list[dict]

Read recent events from the history file, newest first.

```python
for event in ev.history(limit=10):
    print(event["type"], event["timestamp"])
```

## list_types() -> list[str]

Return all known event type names.

```python
ev.list_types()
# -> ["build_result", "job_done", "scholar_done", "stats_done", "test_complete"]
```

## get_type_info(event_type) -> dict

Return metadata (description, expected payload keys) for an event type.

```python
ev.get_type_info("test_complete")
# -> {"description": "Test suite completed (local or HPC)",
#     "payload_keys": ["exit_code", "module", "log_tail"]}
```
