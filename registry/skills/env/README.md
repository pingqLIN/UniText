# Environment (env) Skill

A comprehensive skill for understanding and managing your GitHub Copilot CLI environment configuration.

## Quick Start

**View your complete environment:**
```
/env
```

This shows all loaded environment components and their configuration status.

## What This Skill Does

The `env` skill provides documentation and reference material about:

- **Where configuration files are stored** in `~/.copilot/`
- **What environment components are available** (instructions, MCP servers, skills, agents, etc.)
- **How to troubleshoot** missing or misconfigured tools
- **Best practices** for environment management

## Usage

### Basic Environment Check
```
/env
```
Shows your current environment including:
- Instructions loaded from various locations
- Active MCP servers
- Available skills
- Registered agents
- Installed plugins
- Configured language servers
- Loaded extensions

### Managing Environment Components

Once you understand your environment via `/env`, use these commands to configure:

- **`/skills`** - Enable/disable skills and discover new ones
- **`/mcp`** - Configure Message Context Protocol servers
- **`/instructions`** - View and manage custom instructions
- **`/agent`** - Browse and select agents
- **`/lsp`** - Configure language servers for code intelligence
- **`/plugin`** - Manage plugins and plugin marketplaces

## Key Concepts

### Environment Storage Locations

All Copilot configuration lives in your home directory:

```
~/.copilot/
├── config.json              # Main configuration
├── mcp-config.json          # MCP server setup
├── lsp-config.json          # Language server config (optional)
├── skills/                  # Installed skills
├── session-state/           # Session history and artifacts
└── (other system files)
```

### Instruction File Precedence

Copilot loads instructions in this order (first found wins):
1. `CLAUDE.md` (Claude-specific)
2. `GEMINI.md` (Gemini-specific)
3. `AGENTS.md` (in git root or cwd)
4. `.github/instructions/**/*.instructions.md` (modular)
5. `.github/copilot-instructions.md`
6. `~/.copilot/copilot-instructions.md` (user-level)
7. Directories specified in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` env var

### Configuration Files

**Main config**: `~/.copilot/config.json`
- Model selection
- Theme (light/dark)
- Experimental features enabled/disabled

**MCP servers**: `~/.copilot/mcp-config.json`
- External service integrations
- Custom tools and capabilities

**LSP servers**: `~/.copilot/lsp-config.json`
- Code intelligence providers
- Per-language server configuration

**Permissions**: `~/.copilot/permissions-config.json`
- Allowed tools
- Allowed directories
- Allowed URLs

## Common Tasks

### Verify a Skill is Installed
```
/env
```
Look for the skill name in the output, then use:
```
/skills
```
to enable or disable it.

### Check What Instructions Are Loaded
```
/env
```
Review the "Instructions" section to see which files are being used.

### Configure a New MCP Server
1. First understand your environment: `/env`
2. Then configure the server: `/mcp`
3. Add the server configuration

### Debug Missing Tools
1. Run `/env` to see what's currently loaded
2. Check if the tool appears in the relevant section
3. If missing, use the appropriate management command:
   - Tool not showing? Check `/skills`
   - Server not available? Check `/mcp`
   - Instructions not loaded? Check `/instructions`

## Related Documentation

- **SKILL.md** - Main skill documentation with detailed usage
- **reference.md** - Technical reference for configuration files and structure
- **README.md** (this file) - Quick start and common tasks

## See Also

- GitHub Copilot CLI docs: https://docs.github.com/copilot/concepts/agents/about-copilot-cli
- MCP Servers: Learn more with `/mcp` command
- Custom Instructions: Learn more with `/instructions` command
- Skills: Discover more with `/skills` command

## Troubleshooting

### Environment Not Showing Expected Components

**Problem**: A skill, MCP server, or instruction isn't showing up when you run `/env`

**Solutions**:
1. Check that the component is installed/enabled via its management command
2. Verify file permissions on `~/.copilot/` directory
3. Check JSON syntax in configuration files
4. Try running `/init` to reinitialize configuration
5. Check logs in `~/.copilot/logs/`

### Configuration Won't Save

**Problem**: Changes to environment configuration don't persist

**Solutions**:
1. Ensure `~/.copilot/` directory is writable: `ls -la ~/.copilot/`
2. Check config file permissions
3. Verify JSON syntax in your configuration
4. Restart Copilot CLI
5. Review system permissions for home directory

### Tools Slow to Load

**Problem**: `/env` or other commands are slow

**Solutions**:
1. Check if you have too many MCP servers active (disable unused ones via `/mcp`)
2. Review logs for errors: `~/.copilot/logs/`
3. Check disk space availability
4. Try running `/init` to reset to defaults
5. Check for large files in `~/.copilot/session-state/`
