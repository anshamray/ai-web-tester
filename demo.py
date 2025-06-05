#!/usr/bin/env python3
"""
LangTest Demo - Interactive Web Analysis & Test Generation

This demo script provides an interactive way to test the LangTest tool
with various websites and options.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from main import main

def demo():
    """Interactive demo for LangTest"""
    
    print("🎯 LANGTEST INTERACTIVE DEMO")
    print("=" * 50)
    print("Welcome to LangTest - AI-Powered Web Analysis & Test Generation!")
    print()
    
    # Predefined demo sites
    demo_sites = [
        {
            "name": "Books to Scrape",
            "url": "https://books.toscrape.com",
            "description": "E-commerce site with books, pagination, and forms"
        },
        {
            "name": "HTTPBin Forms",
            "url": "https://httpbin.org/forms/post",
            "description": "Simple form testing site"
        },
        {
            "name": "Example.com",
            "url": "https://example.com",
            "description": "Basic static website"
        },
        {
            "name": "GitHub",
            "url": "https://github.com",
            "description": "Complex web application with many features"
        }
    ]
    
    print("📋 Available Demo Sites:")
    for i, site in enumerate(demo_sites, 1):
        print(f"{i}. {site['name']}")
        print(f"   URL: {site['url']}")
        print(f"   Description: {site['description']}")
        print()
    
    try:
        # Site selection
        while True:
            choice = input("Select a site (1-4) or enter 'custom' for your own URL: ").strip()
            
            if choice.isdigit() and 1 <= int(choice) <= len(demo_sites):
                selected_site = demo_sites[int(choice) - 1]
                url = selected_site['url']
                print(f"\n✅ Selected: {selected_site['name']}")
                print(f"🌐 URL: {url}")
                break
            elif choice.lower() == 'custom':
                url = input("Enter your custom URL (include http/https): ").strip()
                if not url.startswith(('http://', 'https://')):
                    print("❌ Please include http:// or https:// in your URL")
                    continue
                print(f"\n✅ Custom URL: {url}")
                break
            else:
                print("❌ Invalid choice. Please try again.")
        
        print()
        
        # Options selection
        print("🔧 Demo Options:")
        print("1. Analysis only (faster)")
        print("2. Analysis + Test Generation (comprehensive)")
        
        while True:
            mode = input("Select mode (1-2): ").strip()
            if mode in ['1', '2']:
                break
            print("❌ Please select 1 or 2")
        
        generate_tests = mode == '2'
        
        # Browser mode
        print()
        print("🖥️  Browser Options:")
        print("1. Headless (faster, no GUI)")
        print("2. With GUI (slower, you can see the browser)")
        
        while True:
            browser_mode = input("Select browser mode (1-2): ").strip()
            if browser_mode in ['1', '2']:
                break
            print("❌ Please select 1 or 2")
        
        headless = browser_mode == '1'
        
        # Build command line arguments
        sys.argv = ['demo.py', url]
        
        if not headless:
            sys.argv.append('--no-headless')
        
        if generate_tests:
            sys.argv.append('--generate-tests')
        
        print()
        print("🚀 Starting LangTest Demo...")
        print(f"   URL: {url}")
        print(f"   Mode: {'Analysis + Test Generation' if generate_tests else 'Analysis Only'}")
        print(f"   Browser: {'Headless' if headless else 'With GUI'}")
        print()
        print("-" * 60)
        
        # Run the main pipeline
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def quick_demo():
    """Quick demo with predefined settings"""
    
    print("⚡ LANGTEST QUICK DEMO")
    print("-" * 30)
    
    # Use books.toscrape.com with test generation
    url = "https://books.toscrape.com"
    
    print(f"🌐 Analyzing: {url}")
    print("🤖 Mode: Analysis + Test Generation")
    print("🖥️  Browser: Headless")
    print()
    
    # Set up arguments
    sys.argv = ['demo.py', url, '--generate-tests']
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Quick demo interrupted")
    except Exception as e:
        print(f"\n❌ Quick demo error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        quick_demo()
    else:
        demo() 