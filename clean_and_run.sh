#!/bin/bash
# 🧹 Clean Cache Script - Bersihkan Python cache dan restart

echo "🧹 Cleaning Python cache and restarting bot..."

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# Clear Python import cache
python3 -c "
import sys
import importlib
# Clear module cache
for module in list(sys.modules.keys()):
    if module.startswith('src'):
        del sys.modules[module]
print('✅ Python cache cleared')
"

echo "🔄 Restarting bot..."
python3 main.py