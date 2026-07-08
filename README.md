# Dotfiles

Personal dotfiles for macOS development environment.

## What's Included

- **`.zshrc`** - Zsh configuration with Homebrew and mise integration
- **`.zprofile`** - Zsh profile with Homebrew environment setup
- **`.config/mise`** - mise (development environment manager) configuration
- **`.cursor`** - Cursor IDE configuration (settings, extensions, commands)
- **`Brewfile`** - Homebrew packages and casks management
- **`install.sh`** - Automated installation script
- **`update.sh`** - Easy update script for keeping dotfiles in sync

## Installation

### Quick Setup (New Machine)

```bash
git clone https://github.com/mizoo-snow21/dotfiles.git ~/dotfiles
cd ~/dotfiles
./install.sh
```

`install.sh` first installs Homebrew and the `Brewfile` packages, then links the shell dotfiles and installs tools from mise. This avoids first-run errors on a fresh Mac before `brew` or `mise` exist.

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/mizoo-snow21/dotfiles.git ~/dotfiles
   ```

2. Run the installation script:
   ```bash
   cd ~/dotfiles
   chmod +x install.sh
   ./install.sh
   ```

3. Restart your shell or run:
   ```bash
   source ~/.zprofile
   source ~/.zshrc
   ```

## What the Installation Does

- **Backup Protection**: Creates backups of your existing dotfiles in `~/.dotfiles_backup`
- **Homebrew Management**: Installs Homebrew (if not present) and all packages from `Brewfile`
- **Dotfiles Setup**: Creates symbolic links from your home directory to the dotfiles in this repo after Homebrew is ready
- **mise Tools**: Installs language runtimes and cloud CLIs from `.config/mise/config.toml`
- **Cursor Configuration**: Manages Cursor IDE settings, extensions, and custom commands
- **Git Configuration**: Configures Git if not already set up
- **Development Tools**: Sets up mise for managing multiple language versions without requiring it before installation

## Features

### Shell Configuration
- Custom zsh prompt showing username, architecture, and current directory
- Homebrew integration and completions
- mise for development environment management
- Auto-completions and suggestions

### Development Tools
- mise configuration for managing multiple language versions
- Homebrew package management setup
- Cloud CLIs managed by mise: AWS CLI, Azure CLI, and Google Cloud CLI
- Language/runtime tools managed by mise: Python, Node.js, Go, and uv
- Docker Desktop managed by Homebrew cask

### Cursor IDE Configuration
- IDE settings and preferences
- Installed extensions and their configurations
- Custom commands (like criticalthink.md)
- MCP server configurations (secure, environment variable-based)

### MCP Configuration
- **Secure configuration**: API keys managed via environment variables
- **Multi-tool support**: Unified configuration for Cursor and Claude Desktop/Code
- **Template-based**: JSON templates for Cursor/Claude
- **Setup script**: `./scripts/setup-mcp.sh` automatically configures both tools

### Agent Skills Management
- **Unified management**: Manage skills for Cursor, Claude Code, and Connex
- **List-based**: `skills-list.txt` for tracking installed skills
- **Installation script**: `./scripts/install-agent-skills.sh` for batch installation

### Package Management
- **Brewfile**: Automatically installs all your CLI tools, GUI apps, and utilities
- **Current packages**: gh, mise, Docker Desktop, yarn, zsh enhancements, and more
- **Easy expansion**: Add new packages by editing the Brewfile

## Managing Homebrew Packages

### Adding New Packages
Edit the `Brewfile` and add your desired packages:
```ruby
# CLI tools
brew "package-name"

# GUI applications  
cask "application-name"

# Mac App Store apps
mas "App Name", id: 123456789
```

### Updating Package List
When you install new packages manually, update your Brewfile:
```bash
cd ~/dotfiles
brew bundle dump --force    # Updates Brewfile with current packages
git add Brewfile
git commit -m "Update: Add new packages to Brewfile"
git push
```

### Installing Packages on New Machine
The `install.sh` script automatically installs all packages from the Brewfile.

## Updating Your Dotfiles

### Easy Update (Recommended)
```bash
cd ~/dotfiles
./update.sh
```

This script will:
- Copy any changed dotfiles from your home directory
- Update Brewfile with newly installed packages
- Show you what changed and help you commit/push

### Manual Update
When you modify your shell settings or install new packages:

```bash
cd ~/dotfiles

# Copy updated files manually (if needed)
cp ~/.zshrc .
cp ~/.zprofile .

# Update Brewfile with new packages
brew bundle dump --force

# Commit and push
git add .
git commit -m "Update: describe your changes"
git push
```

## MCP Configuration Setup

### Initial Setup

1. Set environment variables in `~/.zshrc` or `~/.zprofile`:
   ```bash
   export CONTEXT7_API_KEY="your-api-key-here"
   ```

2. Run the setup script:
   ```bash
   cd ~/dotfiles
   ./scripts/setup-mcp.sh
   ```

This will:
- Generate `mcp.json.local` (for Cursor/Claude)
- Create symlinks to both tools:
  - Cursor: `~/.cursor/mcp.json`
  - Claude Desktop/Code: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Keep API keys secure (not in Git)

CodexはMCP設定を行わず、`~/.codex/config.toml`は別途手動管理します。

### Adding New MCP Servers

Edit `.config/mcp/mcp.json.template` and add your server configuration:
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@package/server-name"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

Then run `./scripts/setup-mcp.sh` again.

## Agent Skills Management

### Installing Skills

**Individual installation:**
```bash
npx skills add vercel-labs/agent-skills
```

**Batch installation:**
```bash
cd ~/dotfiles
./scripts/install-agent-skills.sh
```

### Managing Skills List

Edit `.config/agent-skills/skills-list.txt` to add/remove skills:
```
vercel-labs/agent-skills
owner/custom-skill-name
```

Then run the installation script to sync.

## Customization

Feel free to fork this repository and customize it for your own needs. The main files to modify are:

- `.zshrc` - Shell configuration
- `.zprofile` - Environment setup
- `.config/mise/` - Development tools configuration
- `.config/mcp/mcp.json.template` - MCP server configuration template
- `.config/agent-skills/skills-list.txt` - Agent skills list

## Backup

Your original dotfiles are automatically backed up to `~/.dotfiles_backup` during installation.

## Requirements

- macOS
- Git
- Command Line Tools for Git/Homebrew installation
- Zsh (default shell on modern macOS)
