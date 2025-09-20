# Dotfiles

Personal dotfiles for macOS development environment.

## What's Included

- **`.zshrc`** - Zsh configuration with Homebrew and mise integration
- **`.zprofile`** - Zsh profile with Homebrew environment setup
- **`.config/mise`** - mise (development environment manager) configuration
- **`Brewfile`** - Homebrew packages and casks management
- **`install.sh`** - Automated installation script

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

- **Backup Protection**: Creates backups of your existing dotfiles in `~/.dotfiles_backup`
- **Dotfiles Setup**: Creates symbolic links from your home directory to the dotfiles in this repo
- **Homebrew Management**: Installs Homebrew (if not present) and all packages from `Brewfile`
- **Git Configuration**: Configures Git if not already set up
- **Development Tools**: Sets up mise for managing multiple language versions

## Features

### Shell Configuration
- Custom zsh prompt showing username, architecture, and current directory
- Homebrew integration and completions
- mise for development environment management
- Auto-completions and suggestions

### Development Tools
- mise configuration for managing multiple language versions
- Homebrew package management setup

### Package Management
- **Brewfile**: Automatically installs all your CLI tools, GUI apps, and utilities
- **Current packages**: gh, mise, yarn, zsh enhancements, and more
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
