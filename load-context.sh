#!/bin/bash
# KB Conduit - Load workspace context
# Called by session-start hook or manually

CONTEXT_FILE=".kb-context/context.yaml"
LOG_FILE="$HOME/.kb-conduit/logs/session.log"

# Ensure log directory exists
mkdir -p "$HOME/.kb-conduit/logs"

# Check if context file exists
if [ ! -f "$CONTEXT_FILE" ]; then
  # Silent - not every project has context
  exit 0
fi

# Parse workspace name
WORKSPACE=$(grep "^workspace:" "$CONTEXT_FILE" | sed 's/^workspace: *//; s/"//g')

if [ -z "$WORKSPACE" ]; then
  echo "⚠️  Warning: .kb-context/context.yaml exists but workspace not defined"
  exit 1
fi

# Display context loaded
echo ""
echo "📍 KB Context: $WORKSPACE"
echo "📚 Context file: $CONTEXT_FILE"

# Count contexts
CONTEXT_COUNT=$(grep -c "^  - " "$CONTEXT_FILE" | head -1)
echo "📋 Loaded contexts: $CONTEXT_COUNT areas"

# Export for agent awareness
export KB_CONTEXT_FILE="$PWD/$CONTEXT_FILE"
export KB_WORKSPACE="$WORKSPACE"
export KB_LOADED="true"

# Log session start
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat >> "$LOG_FILE" <<EOF
---
timestamp: $TIMESTAMP
workspace: "$WORKSPACE"
context_file: "$CONTEXT_FILE"
pwd: "$PWD"
session_id: code-$$
EOF

echo "✓ Context loaded successfully"
echo ""
