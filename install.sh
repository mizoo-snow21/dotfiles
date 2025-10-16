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

# Cursor configuration
backup_and_link "$DOTFILES_DIR/.cursor" "$HOME/.cursor"

echo "✅ Dotfiles installation completed!"

# ==============================================================================
# Homebrew Setup
# ==============================================================================

echo ""
echo "🍺 Setting up Homebrew..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "📥 Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for this session
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -f "/usr/local/bin/brew" ]]; then
        eval "$(/usr/local/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew is already installed"
fi

# Install packages from Brewfile
if [[ -f "$DOTFILES_DIR/Brewfile" ]]; then
    echo "📦 Installing packages from Brewfile..."
    cd "$DOTFILES_DIR"
    brew bundle install --no-lock
    echo "✅ Homebrew packages installation completed!"
else
    echo "⚠️  No Brewfile found. Skipping package installation."
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
# Final Setup
# ==============================================================================

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 What was installed:"
echo "  • Dotfiles (symlinked to $DOTFILES_DIR)"
echo "  • Homebrew packages from Brewfile"
echo "  • Git configuration"
echo ""
echo "🔄 Please restart your shell or run: source ~/.zshrc"
