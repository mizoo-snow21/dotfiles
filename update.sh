#!/bin/bash

# dotfiles update script
set -e

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🔄 Updating dotfiles from current system..."

# .zshrc/.zprofile/.zshenv/.config/* はホームから dotfiles へシンボリックリンクなので
# コピーは不要 — 編集した時点でリポジトリに反映されている（install.sh の backup_and_link 参照）

# Update Brewfile with current packages
echo ""
echo "🍺 Updating Brewfile..."
cd "$DOTFILES_DIR"
if brew bundle dump --force --file=Brewfile.new 2>/dev/null; then
    # Brewfile には「なぜ brew に置かないか」等の注記が手書きで入っているので dump で上書きしない。
    # 差分だけ見せて、取り込むものは手で Brewfile に足す
    if diff -u Brewfile Brewfile.new > /dev/null; then
        rm "Brewfile.new"
        echo "✅ No change: Brewfile"
    else
        echo "📝 Brewfile と実機の差分（必要な行だけ手で Brewfile に反映する）:"
        diff -u Brewfile Brewfile.new || true
        rm "Brewfile.new"
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
