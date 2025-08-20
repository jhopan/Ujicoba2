#!/data/data/com.termux/files/usr/bin/bash

# 📦 PIP INSTALLER & UPDATER
# Ensure pip is available and updated

echo "📦========================================"
echo "🔧 PIP SETUP & PACKAGE INSTALLER"
echo "📱 Termux Python Package Manager"
echo "========================================"
echo ""

# Function to check command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Ensure Python is installed
echo "🐍 Step 1: Checking Python..."
if ! command_exists python && ! command_exists python3; then
    echo "❌ Python not found! Installing..."
    pkg update -y
    pkg install python -y
    echo "✅ Python installed"
else
    echo "✅ Python available"
    python --version 2>/dev/null || python3 --version
fi

# Step 2: Install/Update pip
echo ""
echo "📦 Step 2: Setting up pip..."

if ! command_exists pip && ! command_exists pip3; then
    echo "❌ pip not found! Installing..."
    
    # Method 1: Try package manager
    echo "🔄 Method 1: Package manager..."
    pkg install python-pip -y 2>/dev/null
    
    if ! command_exists pip; then
        # Method 2: ensurepip
        echo "🔄 Method 2: ensurepip..."
        python -m ensurepip --upgrade 2>/dev/null || python3 -m ensurepip --upgrade 2>/dev/null
    fi
    
    if ! command_exists pip; then
        # Method 3: get-pip.py
        echo "🔄 Method 3: get-pip.py..."
        if command_exists curl; then
            curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
            python get-pip.py
            rm -f get-pip.py
        elif command_exists wget; then
            wget https://bootstrap.pypa.io/get-pip.py
            python get-pip.py
            rm -f get-pip.py
        fi
    fi
    
    if command_exists pip; then
        echo "✅ pip installed successfully"
    else
        echo "❌ pip installation failed"
        echo "💡 Try manual installation:"
        echo "   pkg install python-pip"
        exit 1
    fi
else
    echo "✅ pip already available"
fi

# Step 3: Update pip
echo ""
echo "🔄 Step 3: Updating pip..."
pip install --upgrade pip 2>/dev/null || python -m pip install --upgrade pip 2>/dev/null || echo "⚠️ pip update skipped"

# Step 4: Show pip info
echo ""
echo "📊 Step 4: pip Information..."
pip --version 2>/dev/null || pip3 --version 2>/dev/null || echo "❌ pip version check failed"

# Step 5: Install essential packages
echo ""
echo "📚 Step 5: Installing essential packages..."

PACKAGES=(
    "wheel"
    "setuptools"
    "python-telegram-bot>=20.0"
    "google-api-python-client"
    "google-auth-httplib2"
    "google-auth-oauthlib"
    "aiofiles"
    "aiohttp"
    "python-dotenv"
    "pyyaml"
    "requests"
    "urllib3"
    "certifi"
    "python-dateutil"
    "schedule"
    "psutil"
    "Pillow"
    "tqdm"
)

echo "📦 Installing ${#PACKAGES[@]} packages..."

for package in "${PACKAGES[@]}"; do
    echo "   Installing $package..."
    pip install "$package" 2>/dev/null || echo "   ⚠️ $package skipped"
done

# Step 6: Verify installation
echo ""
echo "✅ Step 6: Verification..."
python -c "import telegram; print('✅ Telegram Bot: OK')" 2>/dev/null || echo "❌ Telegram Bot: Failed"
python -c "import googleapiclient; print('✅ Google API: OK')" 2>/dev/null || echo "❌ Google API: Failed"
python -c "import aiofiles; print('✅ Async Files: OK')" 2>/dev/null || echo "❌ Async Files: Failed"
python -c "import yaml; print('✅ YAML: OK')" 2>/dev/null || echo "❌ YAML: Failed"

echo ""
echo "🎉 pip setup complete!"
echo ""
echo "💡 Usage:"
echo "   pip install <package>    # Install package"
echo "   pip list                 # Show installed packages"
echo "   pip show <package>       # Show package info"
echo "   pip install --upgrade <package>  # Update package"
echo ""
echo "🚀 Ready to start bot!"
