# UE5 project organization

## Suggested content layout

```text
Content/
  ProjectName/
    Core/
    Characters/
    Environment/
    UI/
    Systems/
    Maps/
    Data/
    Dev/
```

Keep third-party content outside the project-owned root so licensing and migration boundaries remain visible.

## Naming

Use a consistent prefix scheme only when it helps search and review. Examples include `BP_`, `WBP_`, `BPI_`, `AC_`, `DA_`, `DT_`, and `M_`. Consistency matters more than a large prefix catalog.

## Moving and renaming assets

1. Work on a version-control branch or backup.
2. Move a small, coherent set.
3. Fix redirectors in the affected folder.
4. Compile/load dependent assets and representative maps.
5. Run a packaged-build smoke test when paths or runtime loading are involved.

Do not delete apparently unused assets solely from a folder view. Soft references, Asset Manager rules, configuration strings, and runtime loads may not be obvious.

## Source control boundary

Track source assets and configuration. Ignore generated directories such as `Binaries`, `DerivedDataCache`, `Intermediate`, and `Saved`. Confirm plugin-specific requirements before generalizing the ignore list.

## Troubleshooting archive

For each meaningful failure, preserve a small postmortem using `VERIFIED_CASE_TEMPLATE.md`. A reproducible failure and its verification evidence are more valuable than an unexplained screenshot.

