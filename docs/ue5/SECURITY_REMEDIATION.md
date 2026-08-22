# Security remediation for Blueprint networking and API calls

## Immediate action

Inspection found a third-party API credential stored in a Blueprint default value. Treat it as compromised even if the project and repository are private.

1. Revoke the old credential in the provider dashboard.
2. Create a replacement only after the architecture no longer ships the credential.
3. Search local source, backups, build output, logs, screenshots, and version history.
4. Repackage only after confirming the old value is absent.

This repository intentionally contains neither the value nor a reversible representation of it.

## Unsafe and safe boundaries

```text
Unsafe
UE Blueprint -> provider API
              credential stored in client asset

Safer
UE Blueprint -> controlled gateway -> provider API
                validates request    owns provider credential
                rate limits          filters response
```

Environment variables on the end user's machine do not make a distributed desktop or Android client secret. If the user controls the machine, the user can inspect the process. A gateway is the normal boundary for protecting a provider credential.

## Sanitized Blueprint request flow

```text
OnRequestStart
 -> Construct request (POST, JSON)
 -> SetRequestObject
 -> Bind OnRequestComplete
 -> ProcessURL(gateway endpoint)

OnRequestComplete
 -> Branch request succeeded
 -> Validate response status and expected schema
 -> Read the required JSON fields with array/object guards
 -> Convert the final string to text
 -> Update UI
 -> Clear busy state
```

Also handle timeout, cancellation, invalid JSON, empty arrays, missing fields, provider errors, and widget destruction before the callback returns.

## Release gates

- privacy scanner passes;
- no credential-like strings in tracked files or Git history;
- no secrets in `.uasset`, `.umap`, cooked packages, config, or logs;
- gateway limits payload size, fields, rate, and response content;
- UI tells the user what data is sent;
- AI output never directly drives safety-critical robot or drone control.
