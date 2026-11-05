---
name: scitex-events
description: |
  [WHAT] Lightweight file-backed event bus for SciTeX scripts — emit, latest, history with structured payloads, no external broker.
  [WHEN] Exchanging file-backed progress, lifecycle and result notifications between scripts.
  [HOW] `from scitex_events import emit, latest, history`.
primary_interface: python
interfaces:
  python: 3
  cli: 0
  mcp: 0
  skills: 2
  hook: 0
  http: 0
tags: [scitex-events]
---

> **Interfaces:** Python ⭐⭐⭐ (primary) · Skills ⭐⭐

# scitex-events

Standalone file-backed event bus for SciTeX, using `scitex-config` for state
paths. Python API and installed skills are provided; the package does not host
a CLI, MCP server or Web API. Its optional webhook is outbound delivery.

## Why

Pipelines and agents need to tell each other "X happened" — `print` is
not structured, log files are not queryable, and rolling your own JSON-
line append is the recipe everyone reinvents.

## Public API

```python
import scitex_events as ev

# Emit — type, then free-form kwargs + structured payload
ev.emit("test_complete", project="figrecipe",
        status="success", payload={"exit_code": 0, "module": "stats"})

# Read
ev.latest("test_complete")
list(ev.history(limit=20))
# history does not accept a type= kwarg; use latest(type) instead

# Schema introspection
ev.list_types()
ev.get_type_info("test_complete")
```

Events persist under `local_state.runtime_path("events", ...)` and are
forwarded if `SCITEX_API_KEY` is set. Define types via `Event` for the
schema-driven flow.

Event types are filename components; read [Python API](03_python-api.md) for
the identifier validation applied before local state access.

## When to use

- ✅ Pipeline step succeeds/fails and a downstream agent needs to know
- ✅ HPC batch script broadcasting progress for late readers
- ❌ In-function return values — use return / raise
- ❌ High-frequency telemetry (>100 Hz) — this is on-disk JSON, not Kafka

## Pitfalls

- **Schemaless payloads** — define the type or document fields in the
  emitter docstring.
- **Polling `latest()` in a hot loop** — cache or use webhooks.
- **Hardcoding `~/.scitex/events/...`** — use `local_state.runtime_path`.

## See also

- `scitex-orochi` — agent message bus that consumes events
- `scitex-notification` — slack/email triggered by events
- General `01_arch_06_local-state-directories.md` — runtime path policy

## Sub-skills

### Core (01–09)
- [01_installation.md](01_installation.md) — install + import sanity check
- [02_quick-start.md](02_quick-start.md) — 30-second tour
- [03_python-api.md](03_python-api.md) — Python API surface
