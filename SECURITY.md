# Security and privacy

Do not report passwords, API keys, private repository links, proprietary UE assets, client data, private logs, or personal data in a public issue.

Before publishing a change, run:

```text
python scripts/check_public_release.py . --history
```

The checker is a safety net, not a guarantee. Review the complete staged diff and repository visibility before publication.
