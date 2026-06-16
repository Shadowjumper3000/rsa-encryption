# Security Policy

## Supported Versions

| Version | Supported          |
|---------|--------------------|
| 2.x     | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

This is an **educational** library and is **not intended for production
cryptographic use**. It does not implement modern safeguards like OAEP padding
or side-channel hardened operations.

If you discover a security-relevant bug nevertheless:

- **Do not** open a public GitHub issue.
- Email the maintainer at **shadowjumper3000@gmail.com** with details.
- You should receive a response within 72 hours.
- If the issue is confirmed, a fix will be prioritized and released as a
  patch version. The maintainer will credit you in the release notes
  (unless you prefer to remain anonymous).

## Scope

This policy covers:

- The `src/rsa_encryption/` library code
- The `cli.py` entrypoint
- Build and release infrastructure (GitHub Actions, PyPI publishing)

Out of scope:

- Third-party dependencies (there are none)
- Downstream applications using this library

## Disclosure Timeline

1. **Report received**: maintainer acknowledges within 72 hours.
2. **Triage**: within 7 days.
3. **Fix**: patch released within 30 days of triage (or a clear rationale
   for the delay is provided).
4. **Public disclosure**: after the fix is released.
