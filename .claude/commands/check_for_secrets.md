---
description: Scan staged/tracked files for accidentally committed secrets (API keys, passwords, tokens, etc.)
---

# Check for Secrets

Scan the repository for accidentally committed secrets that should not be pushed to GitHub.

## Process:

1. **Identify files to scan:**
   - Run `git status` to see all tracked and staged changes
   - Run `git diff --name-only HEAD` to see modified files
   - Also check `git diff --cached --name-only` for staged files
   - Focus on these changed files, but also spot-check any config files or source files that commonly contain secrets

2. **Scan for secrets using these patterns:**

   Search all non-gitignored, non-binary tracked files for:

   - **API keys**: patterns like `api_key`, `apikey`, `api-key` followed by assignment to a literal string value
   - **Secret keys**: `secret_key`, `secret`, `client_secret` assigned to literal values
   - **Tokens**: `token`, `access_token`, `auth_token`, `bearer` assigned to literal values
   - **Passwords**: `password`, `passwd`, `pwd` assigned to literal values
   - **Connection strings**: database URLs, Redis URLs, or other service URIs containing credentials
   - **AWS credentials**: `AKIA`, `aws_access_key_id`, `aws_secret_access_key` with literal values
   - **Private keys**: `BEGIN RSA PRIVATE KEY`, `BEGIN OPENSSH PRIVATE KEY`, `BEGIN EC PRIVATE KEY`
   - **Account/project IDs**: `account_id`, `project_id` assigned to specific numeric or alphanumeric values (not placeholders)
   - **Webhook URLs**: URLs containing `/webhook/` or secret tokens in query params
   - **Base64-encoded secrets**: long base64 strings assigned to secret-sounding variable names
   - **Hardcoded IPs/hosts**: internal IPs or hostnames that reveal infrastructure

   **Exclude from flagging:**
   - References to environment variables (e.g., `os.environ["API_KEY"]`, `os.getenv("TOKEN")`)
   - Placeholder values (e.g., `"your-api-key-here"`, `"changeme"`, `"xxx"`, `"..."`)
   - Empty strings or None values
   - Comments explaining what keys are for (without actual values)
   - Values in `.env.example` files (these are templates)
   - Test fixtures with clearly fake values

3. **Check .gitignore coverage:**
   - Verify `.env` is in `.gitignore`
   - Verify any other secret-containing files are ignored
   - Flag if `.env` exists but is NOT in `.gitignore`

4. **Report findings:**

   If secrets are found:
   ```
   ## SECRETS DETECTED

   | File | Line | Type | Value (redacted) |
   |------|------|------|------------------|
   | src/config.py | 12 | API Key | sk-...a3f2 |

   ### Recommended actions:
   1. Remove the secret from the file
   2. Use environment variables instead: `os.getenv("KEY_NAME")`
   3. If already committed, rotate the secret immediately
   ```

   If no secrets found:
   ```
   ## No secrets detected

   Scanned [N] files. No hardcoded secrets, API keys, or credentials found.
   .gitignore properly excludes .env files.
   ```

## Important:
- When showing detected secrets, **redact the middle portion** — only show first 4 and last 4 characters
- Never print full secret values in output
- Check ALL source files, not just recently changed ones
- Pay special attention to: `.py`, `.json`, `.yaml`, `.yml`, `.toml`, `.cfg`, `.ini`, `.conf` files
