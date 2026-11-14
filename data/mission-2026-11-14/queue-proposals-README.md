# Research queue proposals

Agents propose new research questions by writing their own file `queue-proposals-<workstream>.csv` in this directory, using these columns. Each agent writes only its own file, so concurrent agents never conflict.

`question_id,question,area,importance,p_change,gap,commercial,availability,effort,depends_on,breadth_gap,state,assigned_to,conclusion_affected,proposed_by,rationale,evidence_pointer`

The scoring fields use the same scales as `research-priority-inputs.csv`:
- `importance`, `gap`, `commercial`, `availability` and `effort` are 1–5.
- `p_change` is 0–1.
- `state` is `open`.

`question_id` uses the prefix `P-<workstream>-NN`.

`scripts/mission_merge_queue.py` deduplicates the proposals against the existing queue and merges them into `research-priority-inputs.csv`, then re-ranks the queue.
