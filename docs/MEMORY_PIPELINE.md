# Memory Pipeline

This document describes the current memory flow in `aim-codex`.

## Storage Layers
1. Raw transcripts and mirrored archive material
2. Searchable fragment storage in `archive/engram.db`
3. Continuity artifacts in `continuity/`
4. Durable memory in `core/MEMORY.md`

## Main Components
- `scripts/session_porter.py`
- `scripts/extract_signal.py`
- `hooks/tier1_hourly_summarizer.py`
- `src/handoff_pulse_generator.py`
- `src/tier2_daily_summarizer.py`
- `src/tier3_weekly_summarizer.py`
- `src/tier4_memory_proposer.py`

## Flow
1. Session material is mirrored into `archive/raw/`.
2. `extract_signal.py` and related indexers create searchable fragments.
3. Summarizers condense recent activity into continuity and memory artifacts.
4. Retrieval reads from `archive/engram.db` when context is needed.

## Current Rule
One transcript path, one retrieval store, one continuity layer. If those diverge, the pipeline is wrong.
