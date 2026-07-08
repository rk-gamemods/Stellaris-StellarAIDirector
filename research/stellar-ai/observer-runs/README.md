# Observer Runs

Each subfolder is one preserved Stellar AI Director observer experiment. Keep failed runs; failed evidence is often the fastest path to the next useful patch.

Create a new run with:

```powershell
python tools\new_stellar_ai_observer_run.py
```

Refresh the latest run summary with:

```powershell
python tools\summarize_stellar_ai_observer_run.py
```

Standard layout:

```text
<run-id>/
  README.md
  metadata.json
  manual-notes.md
  checkpoints.csv
  metrics.json
  summary.json
  summary.md
  logs/
  saves/
  screenshots/
  exports/
```

Use `checkpoints.csv` for structured benchmark rows and `manual-notes.md` for console-command verification, qualitative behavior notes, and patch hypotheses.
