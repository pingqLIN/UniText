---
runtime_projection: true
source_of_truth: registry/skills/env/reference.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/env/reference.md`
> Source of truth: `registry/skills/env/reference.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Environment Skill Reference

## Complete File Structure

```
~/.copilot/
├── config.json                      # Main CLI configuration
├── config.json.bak                  # Backup of config
├── mcp-config.json                  # MCP server configuration
├── permissions-config.json          # Tool and path permissions
├── command-history-state.json       # Command history
├── session-store.db                 # Session database
├── session-store.db-shm             # Database shared memory
├── session-store.db-wal             # Database write-ahead log
├── copilot-instructions.md          # User-level custom instructions
├── lsp-config.json                  # LSP server configuration
├── skills/                          # Directory of available skills
│   ├── env/                         # Environment skill
│   ├── pdf/                         # PDF processing skill
│   ├── azure-deploy/                # Azure deployment skill
│   └── ... (many more)
├── session-state/                   # Session storage and artifacts
│   ├── [session-id]/
│   │   ├── plan.md                  # Session plan
│   │   └── files/                   # Session artifacts
├── ide/                             # IDE integration data
├── logs/                            # CLI logs
├── pkg/                             # Package data
└── restart/                         # Restart state
```

## Configuration File Details

### config.json
Stores general Copilot CLI settings including:
- Default model selection
- Theme preferences
- Experimental mode status
- Session preferences

### mcp-config.json
Example structure for MCP server configuration:
```json
{
  "mcpServers": {
    "example-server": {
      "command": "node",
      "args": ["/path/to/server.js"],
      "env": {}
    }
  }
}
```

### permissions-config.json
Controls which tools and directories are allowed:
```json
{
  "allowedTools": ["bash", "powershell"],
  "allowedDirectories": ["/home/user/projects"],
  "allowedUrls": []
}
```

### lsp-config.json
Repository or user-level LSP configuration:
```json
{
  "lspServers": {
    "typescript": {
      "command": "typescript-language-server",
      "args": ["--stdio"],
      "fileExtensions": {
        ".ts": "typescript",
        ".tsx": "typescript"
      }
    }
  }
}
```

## Environment Variable Integration

### COPILOT_CUSTOM_INSTRUCTIONS_DIRS
Point to additional directories containing instruction files:
```bash
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="/path/to/instructions:/another/path"
```

### GH_TOKEN / GITHUB_TOKEN
Authentication for GitHub operations:
```bash
export GH_TOKEN="ghp_xxxxxxxxxxxx"  # Fine-grained PAT
```

### LSP Server Environment Variables
Pass through to LSP servers:
```json
{
  "lspServers": {
    "example": {
      "env": {
        "CUSTOM_VAR": "value"
      }
    }
  }
}
```

## Skills Directory Structure

Each skill typically contains:
- `SKILL.md` - Main documentation (required)
- `reference.md` - Detailed reference (optional)
- `LICENSE.txt` - License information
- Supporting scripts or code files

### Creating a Custom Skill

Minimal skill structure:
```
~/.copilot/skills/my-skill/
├── SKILL.md           # Frontmatter + documentation
└── (optional files)
```

SKILL.md frontmatter:
```yaml
---
name: my-skill
description: Brief description of what this skill does
license: MIT
---
```

## Session State Management

### Session Database Location
`~/.copilot/session-state/`

Each session gets:
- Unique session ID (UUID)
- `plan.md` - Implementation plan
- `files/` - Artifacts and temporary files

### Accessing Sessions
```
/session              # View and manage sessions
/resume               # Switch to different session
/session list         # List all sessions
/session info <id>    # Get session details
```

## Troubleshooting Commands

### Quick Diagnostics
```
/env                  # Show all loaded environment components
/lsp                  # Check LSP server status
/mcp                  # Review MCP server configuration
/context              # Show context window usage
/version              # Display version information
/permissions          # Check current permissions
```

### Configuration Validation
```
/init                 # Initialize/reset configuration
/instructions         # View and manage instructions
/allow-all            # Enable all permissions
/reset-allowed-tools  # Reset tool permissions
```

## Performance Optimization

### Reducing Startup Time
1. Remove unused skills via `/skills`
2. Disable unused MCP servers via `/mcp`
3. Check `~/.copilot/logs/` for slowness indicators

### Memory Management
1. Run `/compact` to summarize conversation history
2. Clean up old sessions in `~/.copilot/session-state/`
3. Monitor database files in `~/.copilot/`

## Integration Points

### With IDE
- Configure via `/ide` command
- Settings stored in `~/.copilot/ide/`
- Workspace integration for editor connections

### With Git
- Loads instructions from `.github/` directory
- Uses git information for context
- GitHub integration via authenticated token

### With External Tools
- MCP servers bridge to external systems
- LSP servers provide code intelligence
- Custom instructions extend capabilities
