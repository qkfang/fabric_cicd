# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| Latest on `main` | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do NOT** open a public GitHub issue.
2. Email your findings to **[security contact email]** with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
3. You will receive an acknowledgement within **48 hours**.
4. A fix will be prioritised and released as soon as practical.

## Security Best Practices (for contributors)

- Never commit secrets, tokens, or credentials to this repository.
- All service principal credentials must be stored in **GitHub Secrets** (or equivalent vault).
- Review `config/parameter.yml` before merging — it must not contain real connection strings or passwords.
- Use per-environment service principals with least-privilege Fabric workspace roles.
- Rotate service principal secrets on a regular cadence (90 days recommended).
