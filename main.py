#!/usr/bin/env python3
"""
LangTest - AI-Powered Web Analysis & Test Generation

This script provides comprehensive web analysis and automated test code generation
using AI agents to analyze websites and create production-ready test suites.

Usage:
    python main.py https://example.com
    python main.py https://example.com --generate-tests
    python main.py https://example.com --generate-tests --output-dir my_tests
"""

import asyncio
import sys
import argparse
import os
from pathlib import Path
from base_agent import WebAnalysisAgent
from test_code_generator import TestCodeGenerator
from config import Config
import json

async def main():
    """Main function with integrated web analysis and test generation"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI-powered web analysis with automated test generation')
    parser.add_argument('url', help='URL of the website to analyze')
    parser.add_argument('--headless', action='store_true', default=True, 
                       help='Run browser in headless mode (default)')
    parser.add_argument('--no-headless', action='store_false', dest='headless',
                       help='Run browser with GUI')
    parser.add_argument('--generate-tests', action='store_true',
                       help='Generate automated test code after analysis')
    parser.add_argument('--output-dir', default='generated_tests',
                       help='Output directory for generated tests (default: generated_tests)')
    parser.add_argument('--skip-analysis', action='store_true',
                       help='Skip analysis and generate tests from existing report')
    parser.add_argument('--report-file', 
                       help='Use specific report file for test generation')
    
    args = parser.parse_args()
    
    # Set browser mode
    Config.BROWSER_HEADLESS = args.headless
    
    print("🚀 LangTest - AI-Powered Web Analysis & Test Generation")
    print(f"🌐 Target URL: {args.url}")
    print(f"🖥️  Browser mode: {'headless' if args.headless else 'with GUI'}")
    if args.generate_tests:
        print(f"🤖 Test generation: enabled")
        print(f"📁 Output directory: {args.output_dir}")
    print("-" * 60)
    
    try:
        report = None
        
        # Step 1: Web Analysis (unless skipped)
        if not args.skip_analysis:
            print("\n" + "="*60)
            print("📊 PHASE 1: WEB ANALYSIS")
            print("="*60)
            
            agent = WebAnalysisAgent()
            report = await agent.analyze_website(args.url)
            
            print("\n✅ Web analysis completed successfully!")
            print_analysis_summary(report)
        
        # Step 2: Test Code Generation (if requested)
        if args.generate_tests:
            print("\n" + "="*60)
            print("🤖 PHASE 2: TEST CODE GENERATION")
            print("="*60)
            
            # Load report if not from analysis
            if report is None:
                if args.report_file:
                    report_path = args.report_file
                else:
                    # Find the most recent report for the URL
                    report_path = find_latest_report(args.url)
                
                if not report_path or not os.path.exists(report_path):
                    print(f"❌ No report found. Please run analysis first or specify --report-file")
                    sys.exit(1)
                
                print(f"📄 Loading report: {report_path}")
                with open(report_path, 'r', encoding='utf-8') as f:
                    report = json.load(f)
            
            # Generate test code
            generator = TestCodeGenerator()
            result = await generator.generate_test_code(report, args.output_dir)
            
            print("\n✅ Test code generation completed!")
            print_generation_summary(result)
            
            # Provide next steps
            print("\n" + "="*60)
            print("🚀 NEXT STEPS")
            print("="*60)
            print(f"1. Navigate to test directory:")
            print(f"   cd {result['output_directory']}")
            print(f"")
            print(f"2. Install test dependencies:")
            print(f"   python run_tests.py --install")
            print(f"   # or manually: pip install -r requirements.txt && playwright install")
            print(f"")
            print(f"3. Run the tests:")
            print(f"   python run_tests.py                    # Run all tests")
            print(f"   python run_tests.py --smoke           # Run smoke tests only")
            print(f"   python run_tests.py --integration     # Run integration tests only")
            print(f"   python run_tests.py --html            # Generate HTML report")
            print(f"")
            print(f"4. View test documentation:")
            print(f"   cat README.md")
        
        print("\n" + "="*60)
        print("🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n⏹️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def print_analysis_summary(report: dict):
    """Print summary of web analysis results"""
    
    page_info = report.get('page_info', {})
    test_cases = report.get('test_cases', {})
    
    print(f"\n📊 ANALYSIS SUMMARY")
    print(f"   🌐 Site: {page_info.get('title', 'N/A')}")
    print(f"   ⏱️  Load time: {page_info.get('load_time', 0):.2f}s")
    print(f"   🔗 Links: {page_info.get('links_count', 0)}")
    print(f"   🖼️  Images: {page_info.get('images_count', 0)}")
    print(f"   📝 Forms: {page_info.get('forms_count', 0)}")
    
    if 'test_cases' in test_cases:
        tc_list = test_cases['test_cases']
        print(f"\n🧪 TEST CASES IDENTIFIED")
        print(f"   📊 Total: {len(tc_list)}")
        
        # Count by priority
        priorities = {}
        types = {}
        for tc in tc_list:
            priority = tc.get('priority', 'unknown')
            tc_type = tc.get('type', 'unknown')
            priorities[priority] = priorities.get(priority, 0) + 1
            types[tc_type] = types.get(tc_type, 0) + 1
        
        print(f"   🎯 Priorities: {', '.join([f'{k}({v})' for k, v in priorities.items()])}")
        print(f"   🔍 Types: {', '.join([f'{k}({v})' for k, v in types.items()])}")
        
        if 'summary' in test_cases and 'estimated_total_time' in test_cases['summary']:
            print(f"   ⏱️  Estimated time: {test_cases['summary']['estimated_total_time']}")
    
    # Show potential issues
    bugs = report.get('potential_bugs', [])
    if bugs:
        print(f"\n🐛 POTENTIAL ISSUES: {len(bugs)}")
        for bug in bugs[:3]:  # Show first 3
            print(f"   • {bug.get('description', 'Unknown issue')} ({bug.get('severity', 'unknown')})")
    
    broken_links = report.get('broken_links', [])
    if broken_links:
        print(f"\n❌ BROKEN LINKS: {len(broken_links)}")

def print_generation_summary(result: dict):
    """Print summary of test code generation results"""
    
    print(f"\n🤖 GENERATION SUMMARY")
    print(f"   📁 Output directory: {result['output_directory']}")
    print(f"   📄 Files generated: {len(result['files_generated'])}")
    print(f"   🧪 Test types: {', '.join(result['test_types'])}")
    print(f"   📊 Total test cases: {result['total_test_cases']}")
    
    print(f"\n📁 GENERATED FILES:")
    for file_path in result['files_generated']:
        filename = os.path.basename(file_path)
        print(f"   • {filename}")

def find_latest_report(url: str) -> str:
    """Find the latest report file for a given URL"""
    
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        return None
    
    # Extract domain from URL for matching
    from urllib.parse import urlparse
    domain = urlparse(url).netloc.replace('www.', '')
    
    # Find matching report files
    matching_files = []
    for filename in os.listdir(reports_dir):
        if filename.startswith(f"report_{domain}") and filename.endswith(".json"):
            filepath = os.path.join(reports_dir, filename)
            matching_files.append((filepath, os.path.getmtime(filepath)))
    
    if not matching_files:
        return None
    
    # Return the most recent file
    matching_files.sort(key=lambda x: x[1], reverse=True)
    return matching_files[0][0]

def demo():
    """Demo function for testing the tool"""
    
    print("🎯 LANGTEST DEMO: Web Analysis + Test Generation")
    print("-" * 50)
    
    demo_sites = [
        "https://books.toscrape.com",
        "https://httpbin.org/forms/post",
        "https://example.com"
    ]
    
    print("Available demo sites:")
    for i, site in enumerate(demo_sites, 1):
        print(f"{i}. {site}")
    
    try:
        choice = input("\nSelect site (1-3) or enter custom URL: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(demo_sites):
            url = demo_sites[int(choice) - 1]
        elif choice.startswith('http'):
            url = choice
        else:
            print("❌ Invalid choice")
            return
        
        # Ask about test generation
        gen_tests = input("Generate automated tests? (y/N): ").strip().lower()
        generate_tests = gen_tests in ['y', 'yes']
        
        # Build command line arguments
        sys.argv = ['main.py', url]
        if generate_tests:
            sys.argv.append('--generate-tests')
        
        # Run the pipeline
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No arguments - run demo
        demo()
    else:
        # Run with provided arguments
        asyncio.run(main()) 