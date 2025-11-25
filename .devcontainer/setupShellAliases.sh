#!/usr/bin/env bash

# Set up shell aliases for modern tools
# These tools are installed via the modern-shell-tools devcontainer feature

# Create or append to .zshrc
ZSHRC="$HOME/.zshrc"

# Check if aliases already exist to avoid duplicates
if ! grep -q "# Modern shell tool aliases" "$ZSHRC" 2>/dev/null; then
    cat >> "$ZSHRC" << 'EOF'

# Modern shell tool aliases
alias ls='eza'
alias cat='bat --paging=never'
alias grep='ag'
EOF
    echo "Shell aliases configured successfully"
else
    echo "Shell aliases already configured"
fi
