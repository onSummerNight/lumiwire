---
description: "Write the next task for the worker into docs/BRIEF.md"
argument-hint: "<task>"
disable-model-invocation: true
---
Write the next task for the worker session: $ARGUMENTS

1. Check the task against `docs/CONTEXT.md`. If it is out of scope, say so and stop.
2. Overwrite `docs/BRIEF.md`, 25 lines at most: Goal, Why now, Steps (5 at most), Acceptance check (a command or test), Constraints, Out of scope.
   One task per brief. If it needs more than 5 steps, split it and brief the first part.
3. Append one line to `docs/LOG.md`.
4. Reply with the brief's Goal and Acceptance check, then: "In the worker terminal, type /work".
