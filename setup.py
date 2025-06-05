#!/usr/bin/env python3
"""
Setup script for LangTest

This script helps users set up the LangTest environment quickly.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def setup_environment():
    """Set up the environment"""
    print("\n🚀 Setting up LangTest environment...")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install Playwright browsers
    if not run_command("playwright install", "Installing Playwright browsers"):
        print("⚠️  Playwright installation failed. You may need to install it manually:")
        print("   pip install playwright && playwright install")
    
    # Create .env file if it doesn't exist
    if not Path('.env').exists():
        print("📝 Creating .env file...")
        if Path('.env.example').exists():
            with open('.env.example', 'r') as f:
                env_content = f.read()
            
            with open('.env', 'w') as f:
                f.write(env_content)
            
            print("✅ .env file created from .env.example")
            print("⚠️  Please edit .env and add your OpenAI API key")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file already exists")
    
    # Create necessary directories
    for directory in ['reports', 'exploration_reports', 'generated_tests']:
        Path(directory).mkdir(exist_ok=True)
    print("✅ Created necessary directories")
    
    return True

def verify_setup():
    """Verify the setup is working"""
    print("\n🔍 Verifying setup...")
    
    # Check if OpenAI API key is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key or api_key == 'your-openai-api-key-here':
        print("⚠️  OpenAI API key not configured")
        print("   Please edit .env and add your API key from https://platform.openai.com/api-keys")
        return False
    else:
        print("✅ OpenAI API key configured")
    
    # Test import of main modules
    try:
        from config import Config
        Config.validate()
        print("✅ Configuration validated")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🕷️  LangTest Setup")
    print("=" * 50)
    
    if not setup_environment():
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    
    if not verify_setup():
        print("\n⚠️  Setup completed with warnings. Please check the messages above.")
    else:
        print("\n🎉 Setup completed successfully!")
    
    print("\n📋 Next steps:")
    print("1. Edit .env and add your OpenAI API key")
    print("2. Run a test: python main.py https://example.com")
    print("3. Try the demo: python main.py")
    print("4. Generate tests: python main.py https://example.com --generate-tests")
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main() 