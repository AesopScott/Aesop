#!/bin/bash
# Add cache-busting to all course HTML files

# Get today's date in YYYYMMDD format
CACHE_BUST_TOKEN="cb$(date +%Y%m%d)"

# Convert Windows path to Unix-style for bash
MODULES_PATH="/c/Users/Scott/Code/Aesop/ai-academy/modules"

# Count files
TOTAL=$(find "$MODULES_PATH" -name "*-m*.html" -not -path "*/.claude/worktrees/*" | wc -l)
COUNT=0

echo "Adding cache-busting token: $CACHE_BUST_TOKEN"
echo "Processing $TOTAL files..."

find "$MODULES_PATH" -name "*-m*.html" -not -path "*/.claude/worktrees/*" | while read file; do
    COUNT=$((COUNT + 1))

    # Check if file already has cache-bust token
    if grep -q "cb202[0-9]\{6\}" "$file"; then
        # Update existing cache-bust token
        sed -i "s/cb202[0-9]\{6\}/$CACHE_BUST_TOKEN/g" "$file"
    else
        # Add new cache-bust token to version comment
        # Find the version comment and add cache-bust before the closing -->
        sed -i "s/<!-- v\([0-9.]*\) | \([0-9-]*\) -->$/<!-- v\1 | \2 | $CACHE_BUST_TOKEN -->/g" "$file"
    fi

    if [ $((COUNT % 100)) -eq 0 ]; then
        echo "  Processed: $COUNT/$TOTAL"
    fi
done

echo "✓ Completed: Added cache-busting to $TOTAL course files"
