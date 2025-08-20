#!/data/data/com.termux/files/usr/bin/bash

# 🧪 TEST IMPORT - Verify import paths
# Test semua kemungkinan import path

clear
echo "🧪========================================"
echo "🔍 IMPORT PATH TESTING"
echo "📁 Test all possible import methods"
echo "========================================"
echo ""

cd ~/UjiCoba

echo "📁 Current directory: $(pwd)"
echo "🐍 Python version: $(python --version)"
echo ""

echo "🔍 Step 1: Check file structure..."
echo "📂 Project structure:"
ls -la
echo ""
echo "📂 src/ directory:"
ls -la src/
echo ""
echo "📂 src/telegram/ directory:"
ls -la src/telegram/
echo ""

echo "🧪 Step 2: Test Python imports..."

# Test 1: Standard telegram library
echo "🔗 Test 1: Standard telegram library"
python -c "
try:
    import telegram
    print('✅ Standard telegram library: OK')
    print(f'   Location: {telegram.__file__}')
except Exception as e:
    print(f'❌ Standard telegram: {e}')
"
echo ""

# Test 2: Our custom module dengan sys.path
echo "🔗 Test 2: Custom module with sys.path"
python -c "
import sys
import os
sys.path.insert(0, 'src')
print(f'📁 Working directory: {os.getcwd()}')
print(f'🐍 Python path: {sys.path[:3]}')

try:
    from telegram.termux_telegram_bot import TermuxTelegramBot
    print('✅ Custom termux_telegram_bot: OK')
    print(f'   Class: {TermuxTelegramBot}')
except Exception as e:
    print(f'❌ Custom module: {e}')
    
    # Try to see what's actually in src/telegram
    try:
        import os
        files = os.listdir('src/telegram')
        print(f'📋 Files in src/telegram: {files}')
    except Exception as e2:
        print(f'❌ Cannot list src/telegram: {e2}')
"
echo ""

# Test 3: Direct file import
echo "🔗 Test 3: Direct file import"
python -c "
import importlib.util
import os

if os.path.exists('src/telegram/termux_telegram_bot.py'):
    print('✅ termux_telegram_bot.py file exists')
    
    try:
        spec = importlib.util.spec_from_file_location(
            'termux_telegram_bot', 
            'src/telegram/termux_telegram_bot.py'
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        TermuxTelegramBot = module.TermuxTelegramBot
        print('✅ Direct file import: OK')
        print(f'   Class: {TermuxTelegramBot}')
    except Exception as e:
        print(f'❌ Direct import: {e}')
else:
    print('❌ termux_telegram_bot.py file not found')
"
echo ""

# Test 4: Simple relative import
echo "🔗 Test 4: Simple relative import"
python -c "
import sys
import os
os.chdir('src')
sys.path.insert(0, '.')

try:
    from telegram.termux_telegram_bot import TermuxTelegramBot
    print('✅ Relative import: OK')
except Exception as e:
    print(f'❌ Relative import: {e}')
"
cd ~/UjiCoba
echo ""

echo "🎯 Step 3: Recommended import method..."
echo "Based on tests above, the working import method is:"

python -c "
import sys
import os

# Method that should work
sys.path.insert(0, 'src')
print('📋 Working import method:')
print('   sys.path.insert(0, \"src\")')
print('   from telegram.termux_telegram_bot import TermuxTelegramBot')
print('')

try:
    from telegram.termux_telegram_bot import TermuxTelegramBot
    bot = TermuxTelegramBot()
    print('✅ WORKING: Bot instance created successfully!')
    print(f'   Bot type: {type(bot)}')
except Exception as e:
    print(f'❌ FAILED: {e}')
    print('')
    print('🔧 Alternative method:')
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            'termux_telegram_bot', 
            'src/telegram/termux_telegram_bot.py'
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        TermuxTelegramBot = module.TermuxTelegramBot
        bot = TermuxTelegramBot()
        print('✅ ALTERNATIVE: Direct file import works!')
        print(f'   Bot type: {type(bot)}')
    except Exception as e2:
        print(f'❌ ALTERNATIVE FAILED: {e2}')
"

echo ""
echo "🏁 Import test complete!"
echo "💡 Use the ✅ WORKING method in your scripts"
