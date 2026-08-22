# UE5 organization and cleanup

- Keep project-owned assets under one root and third-party content in identifiable roots.
- Move and rename small groups, then fix redirectors and load representative dependents.
- Inspect hard and soft references, Asset Manager rules, configuration paths, and runtime loading before deletion.
- Keep generated directories out of version control unless a tool or plugin explicitly requires otherwise.
- Record engine version and plugin dependencies with every shared reproduction.
- Prefer a version-control branch or restorable backup before cleanup.
- Package or cook a representative target after changes that affect paths, asset discovery, or runtime loading.

