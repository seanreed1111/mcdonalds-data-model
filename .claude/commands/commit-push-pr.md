---
allowed-tools: Bash(git checkout --branch:*), Bash(git add:*), Bash(git status:*), Bash(git push:*), Bash(git commit:*), Bash(gh pr create:*), Skill(changelog-generator)
description: Commit, push, and open a PR with changelog update
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`

## Your task

Based on the above changes:

### **CRITICAL: Prevent circular dependencies**
**Before doing ANYTHING else, check if CHANGELOG.md is the ONLY file with changes.**
- If CHANGELOG.md is the only modified file, SKIP Phase 2 entirely
- Only proceed to Phase 2 if there are code/feature changes beyond CHANGELOG.md
- This prevents infinite loops: code → changelog → changelog → changelog...

### Phase 0: Secret scan (MUST run before any commits)
**Before creating any commits, scan ALL changed files for accidentally committed secrets.**

Search all non-gitignored changed files for hardcoded secrets:
- **API keys**: `api_key`, `apikey`, `api-key` assigned to literal string values
- **Secret keys**: `secret_key`, `secret`, `client_secret` assigned to literal values
- **Tokens**: `token`, `access_token`, `auth_token`, `bearer` assigned to literal values
- **Passwords**: `password`, `passwd`, `pwd` assigned to literal values
- **Connection strings**: database/Redis/service URIs containing embedded credentials
- **AWS credentials**: `AKIA...` patterns, `aws_access_key_id`, `aws_secret_access_key`
- **Private keys**: `BEGIN RSA PRIVATE KEY`, `BEGIN OPENSSH PRIVATE KEY`, `BEGIN EC PRIVATE KEY`

**Exclude from flagging** (these are NOT secrets):
- Environment variable references (`os.environ[...]`, `os.getenv(...)`)
- Placeholder values (`"your-api-key-here"`, `"changeme"`, `"xxx"`, `"..."`)
- Empty strings or None values
- `.env.example` template files
- Test fixtures with clearly fake values

**If any secrets are detected: STOP IMMEDIATELY.** Do not commit, push, or create a PR. Instead, report:
1. Which file and line contains the secret
2. What type of secret it is
3. The value redacted (first 4 and last 4 characters only)
4. Recommend replacing with `os.getenv("KEY_NAME")` and adding the value to `.env`

**Only proceed to Phase 1 if the secret scan passes with no findings.**

### Phase 1: Create PR (single message)
1. Create a new branch if on main
2. Create a single commit with an appropriate message
3. Push the branch to origin
4. Create a pull request using `gh pr create`
5. You have the capability to call multiple tools in a single response. You MUST do all of the above in a single message.

### Phase 2: Update changelog (conditional - see CRITICAL note above)
**ONLY if changes include files OTHER than CHANGELOG.md:**
6. Invoke the `changelog-generator` skill to update the CHANGELOG.md
7. Add, commit, and push the changelog updates with message: "Update CHANGELOG"

Do not use any other tools or do anything else beyond these steps.
