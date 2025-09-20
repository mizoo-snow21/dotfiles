# Dotfiles

Personal dotfiles for macOS development environment.

## What's Included

- **`.zshrc`** - Zsh configuration with Homebrew and mise integration
- **`.zprofile`** - Zsh profile with Homebrew environment setup
- **`.config/mise`** - mise (development environment manager) configuration

## Installation

### Quick Setup (New Machine)

```bash
git clone https://github.com/YOUR_USERNAME/dotfiles.git ~/dotfiles
cd ~/dotfiles
./install.sh
```

### Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/dotfiles.git ~/dotfiles
   ```

2. Run the installation script:
   ```bash
   cd ~/dotfiles
   chmod +x install.sh
   ./install.sh
   ```

3. Restart your shell or run:
   ```bash
   source ~/.zshrc
   ```

## What the Installation Does

- Creates backups of your existing dotfiles in `~/.dotfiles_backup`
- Creates symbolic links from your home directory to the dotfiles in this repo
- Configures Git if not already set up

## Features

### Shell Configuration
- Custom zsh prompt showing username, architecture, and current directory
- Homebrew integration and completions
- mise for development environment management
- Auto-completions and suggestions

### Development Tools
- mise configuration for managing multiple language versions
- Homebrew package management setup

## Customization

Feel free to fork this repository and customize it for your own needs. The main files to modify are:

- `.zshrc` - Shell configuration
- `.zprofile` - Environment setup
- `.config/mise/` - Development tools configuration

## Backup

Your original dotfiles are automatically backed up to `~/.dotfiles_backup` during installation.

## Requirements

- macOS
- Git
- Homebrew (installed automatically via .zprofile)
- Zsh (default shell on modern macOS)
