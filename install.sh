#!/bin/bash
# KB Conduit Installer

echo "Installing KB Conduit..."
echo ""

# Create KB Conduit directory
mkdir -p ~/.kb-conduit/{templates,logs}

# Copy files
cp load-context.sh ~/.kb-conduit/
cp templates/context.yaml ~/.kb-conduit/templates/
cp README.md ~/.kb-conduit/

# Make executable
chmod +x ~/.kb-conduit/load-context.sh

echo "✓ Files installed to ~/.kb-conduit/"
echo ""
echo "Next steps:"
echo "1. Create context for your project:"
echo "   mkdir -p ~/my-project/.kb-context"
echo "   cp ~/.kb-conduit/templates/context.yaml ~/my-project/.kb-context/"
echo ""
echo "2. Edit context.yaml with your workspace info"
echo ""
echo "3. Load at session start:"
echo "   cd ~/my-project"
echo "   ~/.kb-conduit/load-context.sh"
echo ""
echo "See ~/.kb-conduit/README.md for full documentation"
