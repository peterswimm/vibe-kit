# Troubleshooting

| Issue | Symptom | Fix |
|-------|---------|-----|
| Empty recommendations | Script returns no sessions | Broaden interests or increase time window |
| Overlapping stops | Times collide | Reduce `--stops` or lengthen window |
| Excessive walking time | Large gaps inserted | Adjust buffer variable in script (default 10m) |
| Invalid time window | ValueError raised | Use format `HH:MM-HH:MM` 24h clock |
| Slow scoring with many sessions | Lag in output | Pre-filter by topic similarity threshold |

## Debug Flags (future)
Add `--debug` to print intermediate scores and conflicts.
