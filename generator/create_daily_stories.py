"""Guardrail for the retired batch-prose generator.

Daily stories must be independently planned and written by the scheduled editorial
task.  This module intentionally never emits story bodies: static prose templates
are incompatible with the project's originality requirement.
"""

raise SystemExit(
    "Batch prose generation is disabled. Use generator/editorial-run.md and "
    "generator/topic_scheduler.py to plan independently written stories."
)
