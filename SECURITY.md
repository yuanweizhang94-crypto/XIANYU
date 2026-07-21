# Security Policy

## Sensitive information

- Do not submit Cookie, Token, Secret, private keys, real customer data, or browser credentials.
- Local Profiles, account Profiles, caches, screenshots, logs, cookies, and secrets must not enter Git.
- `.env` must not enter Git; `.env.example` may contain placeholders only.

## Platform boundaries

- Do not bypass platform verification, CAPTCHA, face verification, or risk controls.
- Do not modify device fingerprints.
- Do not automatically rotate proxy IP addresses to avoid detection.
- Stop when risk, credentials, permission, or scope is uncertain.

## Vulnerability reporting

Reports should include impact, sanitized reproduction steps, sanitized logs, and suggested remediation.

## Log handling

Logs must be redacted and must not include secrets, passwords, customer private data, account material, or sensitive Profile paths.
