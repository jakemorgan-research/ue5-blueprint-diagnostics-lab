# Blueprint explanation format

Use the smallest level of detail that lets another person reproduce the reasoning.

## Summary

One sentence describing what the graph tries to accomplish.

## Execution

List the entry event and each meaningful branch, loop, latent action, timer, or callback in order.

## Data

For each important value, state where it comes from, who owns it, whether it can be null/stale, and where it is written.

## Side effects

Identify spawned/destroyed actors, UI updates, saves, audio, animation, physics, network calls, and configuration changes.

## Risks

Separate confirmed failures from plausible risks. Mention hidden dependencies such as editor defaults, child-class overrides, project settings, and replication.

## Verification

Provide one or more observable checks and specify the required run mode.

