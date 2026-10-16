---
name: use-cases
description: Writes use cases that describe how a user and a system interact to reach a goal, including the main flow, alternative flows and failure handling. Use when asked for a use case, a step-by-step interaction description, or when stories alone are too thin for a complex or regulated workflow.
license: MIT
metadata:
  version: "1.0"
---

# Use cases

A use case describes one goal from start to finish, step by step. It is fuller than a user story and good for complex or regulated work.

## Template

```
Name:        verb + object ("Approve a refund")
Actor:       who starts it (primary), others involved (secondary)
Goal:        what the actor wants to achieve
Trigger:     what starts it
Preconditions: what must be true first
Main flow:
  1. Actor ...
  2. System ...
  3. ...
Alternative flows:
  3a. If [condition], then ... (rejoin at step N, or end)
Exceptions:
  4e. If [system fails / data missing], then ...
Postconditions: what is true when it finishes (success) / (failure)
Business rules: BR-12 ...
Frequency / volume:
Open questions:
```

## Rules

- One actor goal per use case; name it with a verb.
- Steps alternate actor and system, in plain words, in the present tense.
- The main flow is the happy path only. Every branch goes in alternatives.
- Do not describe screens or fields; say "enters payment details", not "types in the box on page 3".
- Business rules go in a separate list so they can be reused and changed.
- Keep each between 6 and 12 steps. More means two goals.

## Check

Walk it with someone who does the job. Ask at each step "what else could happen here?" Each answer is an alternative or exception to write down.

## Use with

Use `user-stories` for the backlog and use cases for the detail behind complex ones. Use `process-mapping` to see how several fit together.
