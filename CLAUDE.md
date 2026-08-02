# Claude Code Rules

## Implementation authorization

Implement only an explicitly approved Implementation Task.

Implementation must not begin without explicit implementation-start approval.

## Architecture and scope

Do not independently change the approved architecture.

Do not infer or add Entities, attributes, Protocols, Interfaces, Services, Adapters, repositories, or domain behavior outside the approved task.

Do not add or modify databases, schemas, migrations, or API contracts without explicit approval.

Do not introduce runtime dependencies or AI provider integrations without explicit approval.

## Existing work protection

Do not discard, overwrite, reset, clean, or silently repair existing changes.

Do not modify other repositories unless the approved task explicitly authorizes it.

## Security

Do not open or display `.env` files, credentials, tokens, passwords, API keys, or other secret values.

Do not connect to databases unless explicitly authorized.

## Git

Do not run `git add`, commit, push, change remotes, or create remote repositories without explicit approval.

## Stop and escalate

When required information or authority is missing, stop and submit a Decision Request.

A Decision Request must state:

1. Confirmed facts
2. The unresolved decision
3. Available options
4. Impact of each option
5. Recommended option and rationale
6. Scope that remains unchanged
