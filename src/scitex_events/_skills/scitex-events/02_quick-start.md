---
description: |
  [TOPIC] Quick Start
  [DETAILS] Smallest useful example demonstrating the primary use case in
  under 30 seconds.
tags: [scitex-events-quick-start]
---

# Quick Start

```python
import scitex_events as ev

# Emit an event.
ev.emit("test_complete", project="figrecipe", status="success",
        payload={"exit_code": 0, "module": "stats"})

# Read the latest event of a given type.
latest = ev.latest("test_complete")
print(latest["status"])  # "success"

# Recent history (newest first).
for event in ev.history(limit=5):
    print(event["type"], event["project"])
```
