#!/data/data/com.termux/files/usr/bin/bash

# 🔍 DEBUG HELPER SCRIPT
# Collect system information and debug bot issues

clear
echo "🔍========================================"
echo "🕵️‍♂️ DEBUG & SYSTEM INFORMATION"
echo "🔧 Bot Troubleshooting Helper"
echo "========================================"
echo ""

# Create debug log file
DEBUG_FILE="debug_$(date +%Y%m%d_%H%M%S).log"
echo "📝 Creating debug log: $DEBUG_FILE"
echo ""

# Function to log both to console and file
log_info() {
    echo "$1" | tee -a "$DEBUG_FILE"
}

log_info "=== DEBUG SESSION START ==="
log_info "Date: $(date)"
log_info "User: $(whoami)"
log_info ""

# System Information
log_info "=== SYSTEM INFORMATION ==="
log_info "OS: $(uname -a)"
log_info "Architecture: $(uname -m)"
log_info "Kernel: $(uname -r)"
log_info ""

# Termux Information
log_info "=== TERMUX INFORMATION ==="
log_info "PREFIX: $PREFIX"
log_info "HOME: $HOME"
log_info "TMPDIR: $TMPDIR"
log_info "LD_LIBRARY_PATH: $LD_LIBRARY_PATH"
log_info ""

# Python Information
log_info "=== PYTHON INFORMATION ==="
if command -v python >/dev/null 2>&1; then
    log_info "Python version: $(python --version 2>&1)"
    log_info "Python path: $(which python)"
    log_info "Python executable: $(python -c 'import sys; print(sys.executable)' 2>/dev/null)"
else
    log_info "❌ Python not found"
fi

if command -v python3 >/dev/null 2>&1; then
    log_info "Python3 version: $(python3 --version 2>&1)"
    log_info "Python3 path: $(which python3)"
fi
log_info ""

# Pip Information
log_info "=== PIP INFORMATION ==="
if command -v pip >/dev/null 2>&1; then
    log_info "pip version: $(pip --version 2>&1)"
    log_info "pip path: $(which pip)"
else
    log_info "❌ pip not found"
fi

if command -v pip3 >/dev/null 2>&1; then
    log_info "pip3 version: $(pip3 --version 2>&1)"
    log_info "pip3 path: $(which pip3)"
fi
log_info ""

# Package Information
log_info "=== INSTALLED PACKAGES ==="
if command -v pip >/dev/null 2>&1; then
    log_info "--- All packages ---"
    pip list 2>&1 | tee -a "$DEBUG_FILE"
    
    log_info ""
    log_info "--- Key packages ---"
    pip show python-telegram-bot 2>&1 | grep -E "(Name|Version|Location)" | tee -a "$DEBUG_FILE" || log_info "❌ python-telegram-bot not found"
    pip show google-api-python-client 2>&1 | grep -E "(Name|Version|Location)" | tee -a "$DEBUG_FILE" || log_info "❌ google-api-python-client not found"
    pip show aiofiles 2>&1 | grep -E "(Name|Version|Location)" | tee -a "$DEBUG_FILE" || log_info "❌ aiofiles not found"
else
    log_info "❌ Cannot list packages - pip not available"
fi
log_info ""

# Python Module Test
log_info "=== PYTHON MODULE TEST ==="
python -c "
import sys
print(f'Python version: {sys.version}')
print(f'Python path: {sys.path}')

# Test key modules
modules = ['telegram', 'googleapiclient', 'aiofiles', 'asyncio', 'json', 'os', 'pathlib']
for module in modules:
    try:
        __import__(module)
        print(f'✅ {module}: OK')
    except ImportError as e:
        print(f'❌ {module}: {e}')
" 2>&1 | tee -a "$DEBUG_FILE"
log_info ""

# Process Information
log_info "=== RUNNING PROCESSES ==="
log_info "--- Python processes ---"
ps aux | grep python | grep -v grep | tee -a "$DEBUG_FILE" || log_info "No Python processes running"
log_info ""
log_info "--- Bot processes ---"
ps aux | grep bot | grep -v grep | tee -a "$DEBUG_FILE" || log_info "No bot processes running"
log_info ""

# File System Check
log_info "=== FILE SYSTEM CHECK ==="
log_info "Current directory: $(pwd)"
log_info "Directory contents:"
ls -la | tee -a "$DEBUG_FILE"
log_info ""

if [ -f ".env" ]; then
    log_info "--- .env file exists ---"
    log_info "Size: $(stat -c%s .env 2>/dev/null || echo 'unknown') bytes"
    log_info "Modified: $(stat -c%y .env 2>/dev/null || echo 'unknown')"
    log_info "First few lines (sensitive data hidden):"
    head -5 .env | sed 's/=.*/=***HIDDEN***/' | tee -a "$DEBUG_FILE"
else
    log_info "❌ .env file not found"
fi
log_info ""

if [ -d "credentials" ]; then
    log_info "--- credentials directory ---"
    log_info "Contents:"
    ls -la credentials/ | tee -a "$DEBUG_FILE"
else
    log_info "❌ credentials directory not found"
fi
log_info ""

# Network Check
log_info "=== NETWORK CHECK ==="
if command -v ping >/dev/null 2>&1; then
    log_info "--- Internet connectivity ---"
    ping -c 2 8.8.8.8 >/dev/null 2>&1 && log_info "✅ Internet: OK" || log_info "❌ Internet: Failed"
    ping -c 2 api.telegram.org >/dev/null 2>&1 && log_info "✅ Telegram API: OK" || log_info "❌ Telegram API: Failed"
else
    log_info "⚠️ ping not available"
fi
log_info ""

# Log Files Check
log_info "=== LOG FILES ==="
if [ -d "logs" ]; then
    log_info "--- Recent logs ---"
    ls -la logs/ | tee -a "$DEBUG_FILE"
    
    # Show last few lines of recent log files
    for logfile in logs/*.log; do
        if [ -f "$logfile" ]; then
            log_info "--- Last 5 lines of $(basename "$logfile") ---"
            tail -5 "$logfile" | tee -a "$DEBUG_FILE"
            log_info ""
        fi
    done
else
    log_info "❌ logs directory not found"
fi

# Quick Bot Test
log_info "=== QUICK BOT TEST ==="
log_info "Testing bot initialization..."
python -c "
import sys
sys.path.append('src')
try:
    from telegram.termux_telegram_bot import TermuxTelegramBot
    print('✅ Bot class import: OK')
    
    bot = TermuxTelegramBot()
    print('✅ Bot initialization: OK')
except Exception as e:
    print(f'❌ Bot test failed: {e}')
" 2>&1 | tee -a "$DEBUG_FILE"
log_info ""

log_info "=== DEBUG SESSION END ==="
log_info ""

echo ""
echo "🎉 Debug information collected!"
echo "📝 Saved to: $DEBUG_FILE"
echo ""
echo "📤 To share this debug info:"
echo "   cat $DEBUG_FILE"
echo ""
echo "🔧 Common fixes based on errors:"
echo "   • pip not found: ./scripts/setup_pip.sh"
echo "   • bot stuck: ./scripts/emergency_restart.sh"
echo "   • full reset: rm .env && ./quick_start.sh"
echo ""
echo "📞 Include this debug file when reporting issues!"
