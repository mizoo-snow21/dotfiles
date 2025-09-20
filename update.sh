#!/bin/bash

# dotfiles update script
set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 Updating dotfiles from current system..."

# Function to copy file if it exists and is different
update_file() {
    local source="$1"
    local target="$2"
    local filename=$(basename "$target")
    
    if [[ -f "$source" ]]; then
        if [[ ! -f "$target" ]] || ! cmp -s "$source" "$target"; then
            cp "$source" "$target"
            echo "📝 Updated: $filename"
        else
            echo "✅ No change: $filename"
        fi
    else
        echo "⚠️  Not found: $source"
    fi
}

# Update dotfiles from home directory
echo ""
echo "📁 Updating dotfiles..."
update_file "$HOME/.zshrc" "$DOTFILES_DIR/.zshrc"
update_file "$HOME/.zprofile" "$DOTFILES_DIR/.zprofile"

# Update mise configuration
if [[ -d "$HOME/.config/mise" ]]; then
    if [[ ! -d "$DOTFILES_DIR/.config/mise" ]] || ! diff -r "$HOME/.config/mise" "$DOTFILES_DIR/.config/mise" > /dev/null 2>&1; then
        cp -r "$HOME/.config/mise" "$DOTFILES_DIR/.config/"
        echo "📝 Updated: mise configuration"
    else
        echo "✅ No change: mise configuration"
    fi
fi

# Update Brewfile with current packages
echo ""
echo "🍺 Updating Brewfile..."
cd "$DOTFILES_DIR"
if brew bundle dump --force --file=Brewfile.new 2>/dev/null; then
    if [[ ! -f "Brewfile" ]] || ! cmp -s "Brewfile" "Brewfile.new"; then
        mv "Brewfile.new" "Brewfile"
        echo "📝 Updated: Brewfile with current packages"
    else
        rm "Brewfile.new"
        echo "✅ No change: Brewfile"
    fi
else
    echo "⚠️  Could not update Brewfile (Homebrew not available)"
fi

# Check for changes
echo ""
echo "🔍 Checking for changes..."
if [[ -n $(git status --porcelain) ]]; then
    echo ""
    echo "📋 Changes detected:"
    git status --short
    
    echo ""
    echo "🤔 What would you like to do?"
    echo "1) Review changes (git diff)"
    echo "2) Commit and push changes"
    echo "3) Exit without committing"
    
    read -p "Choose (1-3): " choice
    
    case $choice in
        1)
            echo ""
            echo "📄 Showing changes..."
            git diff
            echo ""
            read -p "Commit these changes? (y/N): " commit_choice
            if [[ $commit_choice =~ ^[Yy]$ ]]; then
                read -p "Enter commit message: " commit_msg
                git add .
                git commit -m "${commit_msg:-Update dotfiles}"
                
                read -p "Push to GitHub? (y/N): " push_choice
                if [[ $push_choice =~ ^[Yy]$ ]]; then
                    git push
                    echo "✅ Changes pushed to GitHub!"
                fi
            fi
            ;;
        2)
            read -p "Enter commit message: " commit_msg
            git add .
            git commit -m "${commit_msg:-Update dotfiles}"
            git push
            echo "✅ Changes committed and pushed!"
            ;;
        3)
            echo "😌 Exiting without committing"
            ;;
        *)
            echo "😌 Invalid choice. Exiting without committing"
            ;;
    esac
else
    echo "✅ No changes detected. Everything is up to date!"
fi

echo ""
echo "🎉 Update complete!"
