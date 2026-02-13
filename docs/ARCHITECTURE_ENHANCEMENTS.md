# Architecture Enhancements (next layers)

## Proposed additional layers

1. **Capability Registry Layer**
   - stores agent capabilities, allowed tools, and skill compatibility.

2. **Policy Decision Layer**
   - produces signed `policy_decision_id` before execution.

3. **Execution Sandbox Layer**
   - isolates tool calls with strict FS/network controls.

4. **Audit & Forensics Layer**
   - immutable event log for route/policy/tool actions.

5. **Quality Evaluation Layer**
   - post-run scoring (faithfulness, compliance, user value).

6. **Experimentation Layer**
   - A/B testing for prompts, routes, and skill chains.

## Why this matters
These layers convert a demo orchestrator into a production-grade AI operations platform.
