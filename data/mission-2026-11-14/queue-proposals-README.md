# Research queue proposals

Agents propose new research questions by writing their own file `queue-proposals-<workstream>.csv` in this directory, using these columns. Each agent writes only its own file, so concurrent agents never conflict.

`question_id,question,area,importance,p_change,gap,commercial,availability,effort,depends_on,breadth_gap,state,assigned_to,conclusion_affected,proposed_by,rationale,evidence_pointer`

The scoring fields use the same scales as `research-priority-inputs.csv`:
- `importance`, `gap`, `commercial`, `availability` and `effort` are 1–5.
- `p_change` is 0–1.
- `state` is `open`.

`question_id` uses the prefix `P-<workstream>-NN`.

`scripts/mission_merge_queue.py` deduplicates the proposals against the existing queue and merges them into `research-priority-inputs.csv`, then re-ranks the queue.

**Recency rule (owner direction, 2026-11-14).** Research targets the current market (2021 onward). Questions whose value depends mainly on pre-2021 history are marked `deprioritized_historical`; they are kept for traceability but not scheduled. New proposals should not request back-histories (e.g. 2011–2020 panels) unless needed to interpret a current figure.
