#!/bin/bash

# dotfiles installation script
set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$HOME/.dotfiles_backup"

set_brew_shellenv() {
    if [[ -x "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -x "/usr/local/bin/brew" ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
}

echo "🚀 Starting dotfiles installation..."
echo "Dotfiles directory: $DOTFILES_DIR"

# Create backup directory
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "📁 Created backup directory: $BACKUP_DIR"
fi

# Function to backup and create symlink
backup_and_link() {
    local source="$1"
    local target="$2"
    
    # Create target directory if it doesn't exist
    local target_dir=$(dirname "$target")
    if [ ! -d "$target_dir" ]; then
        mkdir -p "$target_dir"
    fi
    
    # Backup existing file/dir if it exists and is not a symlink
    if [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "📋 Backing up $target"
        [ -d "$target" ] && cp -r "$target" "$BACKUP_DIR/$(basename "$target").backup" || cp "$target" "$BACKUP_DIR/$(basename "$target").backup"
    fi
    
    # Remove existing file/symlink/dir
    if [ -e "$target" ] || [ -L "$target" ]; then
        rm -rf "$target"
    fi
    
    # Create symlink
    ln -s "$source" "$target"
    echo "🔗 Created symlink: $target -> $source"
}

# ==============================================================================
# Homebrew Setup
# ==============================================================================

echo "🍺 Setting up Homebrew..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "📥 Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    set_brew_shellenv
else
    echo "✅ Homebrew is already installed"
    set_brew_shellenv
fi

# Install packages from Brewfile
if [[ -f "$DOTFILES_DIR/Brewfile" ]]; then
    echo "📦 Installing packages from Brewfile..."
    cd "$DOTFILES_DIR"
    brew bundle install
    echo "✅ Homebrew packages installation completed!"
else
    echo "⚠️  No Brewfile found. Skipping package installation."
fi

# ==============================================================================
# Dotfiles Setup
# ==============================================================================

echo ""
echo "📝 Installing dotfiles..."

backup_and_link "$DOTFILES_DIR/.zprofile" "$HOME/.zprofile"
backup_and_link "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
backup_and_link "$DOTFILES_DIR/.config/mise" "$HOME/.config/mise"
backup_and_link "$DOTFILES_DIR/.config/ghostty" "$HOME/.config/ghostty"
backup_and_link "$DOTFILES_DIR/.config/zellij" "$HOME/.config/zellij"
# .cursor はディレクトリ全体をリンクしない。chats/ projects/ agents/ plans/ など
# Cursor の実行時状態が同居しており、backup_and_link の rm -rf で消えるため。
# リポジトリで持つ意味があるサブディレクトリだけを個別にリンクする。
backup_and_link "$DOTFILES_DIR/.cursor/commands" "$HOME/.cursor/commands"
backup_and_link "$DOTFILES_DIR/.cursor/rules" "$HOME/.cursor/rules"
backup_and_link "$DOTFILES_DIR/.claude" "$HOME/.claude"

echo "✅ Dotfiles installation completed!"

# ==============================================================================
# mise Tools Setup
# ==============================================================================

echo ""
echo "🧰 Installing mise-managed tools..."
if command -v mise &> /dev/null; then
    mise install
    echo "✅ mise-managed tools installation completed!"
else
    echo "⚠️  mise not found. Skipping mise tool installation."
fi

# ==============================================================================
# rtk Setup (LLM token compression proxy)
# ==============================================================================

echo ""
if command -v rtk &> /dev/null; then
    echo "🪚 Setting up rtk..."
    RTK_CONFIG_DIR="$HOME/Library/Application Support/rtk"
    mkdir -p "$RTK_CONFIG_DIR"
    backup_and_link "$DOTFILES_DIR/.config/rtk/config.toml" "$RTK_CONFIG_DIR/config.toml"
    rtk init -g --hook-only --auto-patch                 # Claude Code (RTK.md is tracked in .claude/)
    # Cursor hook is NOT registered here. On this machine the hook fires without any
    # local registration (verified: hooks.json deleted, rtk hook-audit still counts
    # invocations), so adding one would only duplicate it. The allowlist entry below
    # is what actually makes Cursor work, and it is harmless when no hook fires.
    # Cursor evaluates its approval allowlist against the POST-hook command, so every
    # rewritten command needs `Shell(rtk)` allowlisted or headless dispatches reject
    # them all. Cursor's factory default allowlist is just ["Shell(ls)"].
    python3 - <<'RTKPY'
import json, pathlib
p = pathlib.Path.home() / ".cursor/cli-config.json"
if p.exists():
    d = json.loads(p.read_text())
    perm = d.setdefault("permissions", {"allow": [], "deny": []})
    if "Shell(rtk)" not in perm["allow"]:
        perm["allow"].append("Shell(rtk)")
        p.write_text(json.dumps(d, indent=2))
        print("  added Shell(rtk) to Cursor allowlist")
RTKPY
    rtk init -g --opencode --hook-only --auto-patch      # OpenCode
    rtk init -g --codex --auto-patch                     # Codex CLI (instructions-only, no hook)
    # Codex CLI does not expand @-imports in AGENTS.md (verified 2026-08-08), so the
    # reference rtk writes is dead — inline the instructions plus the review carve-out.
    if ! grep -q "Rust Token Killer" "$HOME/.codex/AGENTS.md" 2>/dev/null; then
        cat "$HOME/.codex/RTK.md" >> "$HOME/.codex/AGENTS.md"
        cat "$DOTFILES_DIR/.config/rtk/codex-agents-exception.md" >> "$HOME/.codex/AGENTS.md"
    fi
    echo "✅ rtk hooks installed"
else
    echo "⚠️  rtk not found. Skipping rtk setup."
fi

# ==============================================================================
# Git Configuration
# ==============================================================================

echo ""
if ! git config --global user.name > /dev/null 2>&1; then
    echo "⚙️  Git configuration needed:"
    read -p "Enter your Git username: " git_username
    read -p "Enter your Git email: " git_email
    git config --global user.name "$git_username"
    git config --global user.email "$git_email"
    echo "✅ Git configuration completed!"
else
    echo "✅ Git is already configured"
fi

# ==============================================================================
# MCP Configuration Setup (Optional)
# ==============================================================================

echo ""
if [[ -f "$DOTFILES_DIR/scripts/setup-mcp.sh" ]]; then
    echo "🔧 MCP configuration setup available"
    read -p "Do you want to set up MCP configuration now? (y/N): " setup_mcp
    if [[ "$setup_mcp" =~ ^[Yy]$ ]]; then
        bash "$DOTFILES_DIR/scripts/setup-mcp.sh"
    else
        echo "⏭️  Skipping MCP configuration setup"
        echo "   You can run it later with: ./scripts/setup-mcp.sh"
    fi
fi

# ==============================================================================
# Agent Skills Setup (Optional)
# ==============================================================================

echo ""
if [[ -f "$DOTFILES_DIR/scripts/install-agent-skills.sh" ]]; then
    echo "📚 Agent skills setup available"
    read -p "Do you want to install agent skills now? (y/N): " setup_skills
    if [[ "$setup_skills" =~ ^[Yy]$ ]]; then
        bash "$DOTFILES_DIR/scripts/install-agent-skills.sh"
    else
        echo "⏭️  Skipping agent skills setup"
        echo "   You can run it later with: ./scripts/install-agent-skills.sh"
    fi
fi

# ==============================================================================
# Claude Code MCP Setup (Optional)
# ==============================================================================

echo ""
if [[ -f "$DOTFILES_DIR/scripts/setup-claude-code-mcp.sh" ]]; then
    echo "🔧 Claude Code MCP server setup available"
    read -p "Do you want to register Claude Code CLI MCP servers now? (y/N): " setup_cc_mcp
    if [[ "$setup_cc_mcp" =~ ^[Yy]$ ]]; then
        bash "$DOTFILES_DIR/scripts/setup-claude-code-mcp.sh"
    else
        echo "⏭️  Skipping Claude Code MCP setup"
        echo "   You can run it later with: ./scripts/setup-claude-code-mcp.sh"
    fi
fi

# ==============================================================================
# Claude Code Plugins Setup
# ==============================================================================

echo ""
if [[ -f "$DOTFILES_DIR/scripts/install-claude-plugins.sh" ]]; then
    echo "🔌 Claude Code plugins setup available"
    read -p "Do you want to install Claude Code plugins now? (y/N): " setup_plugins
    if [[ "$setup_plugins" =~ ^[Yy]$ ]]; then
        bash "$DOTFILES_DIR/scripts/install-claude-plugins.sh"
    else
        echo "⏭️  Skipping Claude Code plugins setup"
        echo "   You can run it later with: ./scripts/install-claude-plugins.sh"
    fi
fi

# ==============================================================================
# Final Setup
# ==============================================================================

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 What was installed:"
echo "  • Dotfiles (symlinked to $DOTFILES_DIR)"
echo "  • Homebrew packages from Brewfile"
echo "  • Git configuration"
echo "  • Claude Code plugins (if selected)"
echo ""
echo "🔄 Please restart your shell or run: source ~/.zprofile && source ~/.zshrc"
