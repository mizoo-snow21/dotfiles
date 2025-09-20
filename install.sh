#!/bin/bash

# dotfiles installation script
set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKUP_DIR="$HOME/.dotfiles_backup"

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
    
    # Backup existing file if it exists and is not a symlink
    if [ -e "$target" ] && [ ! -L "$target" ]; then
        echo "📋 Backing up $target"
        cp "$target" "$BACKUP_DIR/$(basename "$target").backup"
    fi
    
    # Remove existing file/symlink
    if [ -e "$target" ] || [ -L "$target" ]; then
        rm -f "$target"
    fi
    
    # Create symlink
    ln -s "$source" "$target"
    echo "🔗 Created symlink: $target -> $source"
}

# Install dotfiles
echo "📝 Installing dotfiles..."

backup_and_link "$DOTFILES_DIR/.zshrc" "$HOME/.zshrc"
backup_and_link "$DOTFILES_DIR/.zprofile" "$HOME/.zprofile"
backup_and_link "$DOTFILES_DIR/.config/mise" "$HOME/.config/mise"

echo "✅ Dotfiles installation completed!"
echo "🔄 Please restart your shell or run: source ~/.zshrc"

# Git configuration prompt
if ! git config --global user.name > /dev/null 2>&1; then
    echo ""
    echo "⚙️  Git configuration needed:"
    read -p "Enter your Git username: " git_username
    read -p "Enter your Git email: " git_email
    git config --global user.name "$git_username"
    git config --global user.email "$git_email"
    echo "✅ Git configuration completed!"
fi
