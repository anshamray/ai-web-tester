# 🕷️ LangTest - AI-Powered Web Analysis & Test Generation

An intelligent web analysis and automated test generation pipeline powered by AI agents. This tool analyzes websites, performs deep exploration with user simulation, and automatically generates comprehensive test suites for quality assurance.

## 🚀 Features

### 🔍 Web Analysis Agent
- **Comprehensive Site Analysis**: Analyzes page structure, forms, links, images, and metadata
- **AI-Powered Insights**: Uses GPT-4 to identify potential issues and testing opportunities
- **Test Case Generation**: Automatically identifies and prioritizes test scenarios
- **Performance Metrics**: Measures load times and identifies performance bottlenecks
- **Accessibility Assessment**: Checks for common accessibility issues
- **SEO Analysis**: Evaluates meta tags and SEO best practices

### 🤖 Smart Exploration Agent (NEW!)
- **🔐 Automatic Registration**: Registers on websites with different user personas
- **📝 Intelligent Form Filling**: Smart form completion with appropriate test data
- **🕵️ Hidden Functionality Discovery**: Finds hidden elements and protected sections
- **🛤️ User Flow Simulation**: Mimics real user behavior for deep testing
- **🔒 Security Analysis**: Analyzes security headers and potential vulnerabilities
- **👥 Multiple User Personas**: Tests with Regular, Power, and Edge Case users

### 🧪 Automated Test Code Generation
- **Playwright Test Generation**: Creates production-ready Playwright tests with pytest
- **Multiple Test Types**: Generates tests for forms, navigation, media, performance, and accessibility
- **Smart Test Organization**: Organizes tests by type with proper fixtures and configuration
- **Comprehensive Documentation**: Auto-generates README, requirements, and setup instructions
- **Test Runner Scripts**: Includes convenient scripts for running different test suites
- **CI/CD Ready**: Generated tests are ready for integration into CI/CD pipelines

## 📦 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd langtest
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
```bash
# Create .env file
echo "OPENAI_API_KEY=your_openai_api_key" > .env
```

4. **Install Playwright browsers** (for test generation):
```bash
playwright install
```

## 🎯 Quick Start

### Basic Web Analysis
```bash
# Analyze a website
python main.py https://example.com

# Run with browser GUI (for debugging)
python main.py https://example.com --no-headless
```

### Smart Deep Exploration (NEW!)
```bash
# Deep exploration with user simulation
python smart_demo.py

# Or programmatically
python -c "
import asyncio
from smart_exploration_agent import SmartExplorationAgent

async def explore():
    agent = SmartExplorationAgent()
    report = await agent.deep_explore_website('https://example.com')
    print(f'Found {len(report[\"registration_attempts\"])} registration attempts')

asyncio.run(explore())
"
```

### Enhanced Pipeline with Test Generation
```bash
# Analyze website AND generate automated tests
python enhanced_main.py https://example.com --generate-tests

# Generate tests from existing report
python enhanced_main.py https://example.com --generate-tests --skip-analysis

# Specify custom output directory
python enhanced_main.py https://example.com --generate-tests --output-dir my_tests
```

### Demo Mode
```bash
# Run interactive demo (no arguments)
python enhanced_main.py

# Smart exploration demo
python smart_demo.py
```

## 📊 Usage Examples

### 1. E-commerce Site Deep Analysis
```bash
python smart_demo.py
# Select "Books to Scrape" for comprehensive e-commerce testing
```
**Smart Agent Features**:
- Automatic user registration with different personas
- Shopping cart form testing
- Product search and filtering
- Hidden functionality discovery
- Security vulnerability assessment

### 2. Corporate Website Analysis
```bash
python enhanced_main.py https://example.com --generate-tests
```
**Generated Tests Include**:
- Contact form validation
- Navigation menu testing
- Content accessibility
- SEO compliance checks

## 🗂️ Project Structure

```
langtest/
├── base_agent.py                    # Core web analysis agent
├── smart_exploration_agent.py       # NEW: Deep exploration with user simulation
├── test_code_generator.py          # Automated test generation agent
├── enhanced_main.py                # Enhanced pipeline with test generation
├── smart_demo.py                   # NEW: Interactive smart exploration demo
├── main.py                         # Original analysis-only pipeline
├── demo.py                         # Basic demo
├── browser_tool.py                 # Playwright browser automation
├── config.py                       # Configuration management
├── reports/                        # Analysis reports (JSON format)
├── exploration_reports/            # NEW: Smart exploration reports
└── generated_tests/                # Auto-generated test suites
    ├── test_*.py                   # Generated test files
    ├── conftest.py                 # Pytest fixtures
    ├── test_config.py              # Test configuration
    ├── run_tests.py                # Test runner script
    ├── requirements.txt            # Test dependencies
    └── README.md                   # Test documentation
```

## 🤖 Smart Exploration Features

### 👥 User Personas
The smart agent uses three different personas for comprehensive testing:

1. **Regular User** - Conservative, careful user behavior
2. **Power User** - Active, experienced user with advanced interactions  
3. **Edge Case User** - Tests with Unicode names, complex data, boundary conditions

### 🔍 Deep Analysis Capabilities
- **Authentication Form Discovery**: Finds login/registration forms across the site
- **Intelligent Form Completion**: Generates appropriate test data for each field type
- **Hidden Element Detection**: Discovers elements with `display: none` or `visibility: hidden`
- **HTML Comment Analysis**: Extracts insights from developer comments
- **User Flow Tracing**: Maps complete user journeys and interactions
- **Security Assessment**: Checks for CSRF protection, security headers, potential vulnerabilities

### 📊 Smart Exploration Report
```json
{
  "url": "https://example.com",
  "timestamp": "2025-06-04T17:18:51.123456",
  "exploration_depth": 3,
  "main_page_analysis": {
    "site_type": "e-commerce",
    "main_sections": ["navigation", "products", "footer"],
    "seo_quality": "good",
    "accessibility_issues": ["missing alt tags"]
  },
  "auth_forms_discovered": 2,
  "registration_attempts": [
    {
      "persona": "regular_user",
      "form_url": "https://example.com/register",
      "test_data": {...},
      "fill_result": "success",
      "submit_result": "form_submitted"
    }
  ],
  "form_interactions": [...],
  "hidden_functionality": [...],
  "user_flows": [...],
  "security_findings": [...],
  "performance_insights": {...}
}
```

## 🧪 Generated Test Structure

When you run test generation, you get a complete test suite:

```
generated_tests/
├── test_form_validation.py    # Form testing (validation, submission)
├── test_navigation.py         # Link and navigation testing
├── test_media.py             # Image and media testing
├── test_performance.py       # Performance and load time testing
├── test_accessibility.py     # Accessibility compliance testing
├── conftest.py               # Pytest fixtures and setup
├── test_config.py            # Test configuration
├── run_tests.py              # Convenient test runner
├── requirements.txt          # Test-specific dependencies
└── README.md                 # Complete test documentation
```

### Running Generated Tests
```bash
cd generated_tests

# Install test dependencies
python run_tests.py --install

# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --smoke           # Quick smoke tests
python run_tests.py --integration     # Integration tests
python run_tests.py --type navigation # Specific test type

# Generate HTML report
python run_tests.py --html
```

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
BROWSER_HEADLESS=true          # Run browser in headless mode
BROWSER_TIMEOUT=30000          # Browser timeout in milliseconds
PAGE_LOAD_TIMEOUT=10000        # Page load timeout for smart agent
```

### Smart Agent Configuration
```python
# In smart_exploration_agent.py, you can customize:
USER_PERSONAS = [
    {
        "name": "custom_user",
        "email_prefix": "customuser",
        "first_name": "Custom",
        "last_name": "User",
        "behavior": "custom"
    }
]
```

## 🛡️ Security and Ethics

### ⚠️ Important Warnings
- **Use only on your own websites** or with explicit permission from the owner
- **Do not use for hacking** or unauthorized access
- **Respect robots.txt** and website terms of service
- **Do not overload servers** - use reasonable delays

### 🔒 Security Recommendations
- Use test email addresses (e.g., @testmail.com)
- Do not use real personal data
- Run in isolated environments
- Regularly clean generated data

## 🚀 Advanced Usage

### Custom Smart Exploration
```python
from smart_exploration_agent import SmartExplorationAgent
import asyncio

async def custom_exploration():
    agent = SmartExplorationAgent()
    
    # Deep exploration with custom depth
    report = await agent.deep_explore_website(
        url="https://example.com",
        max_depth=5
    )
    
    print(f"Registration attempts: {len(report['registration_attempts'])}")
    print(f"Forms discovered: {len(report['form_interactions'])}")
    print(f"Security findings: {len(report['security_findings'])}")

asyncio.run(custom_exploration())
```

### Batch Processing
```bash
# Analyze multiple sites with smart exploration
for url in "https://site1.com" "https://site2.com" "https://site3.com"; do
    python -c "
import asyncio
from smart_exploration_agent import SmartExplorationAgent

async def explore():
    agent = SmartExplorationAgent()
    await agent.deep_explore_website('$url')

asyncio.run(explore())
"
done
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the generated README files in test directories
- **Examples**: See the demo files for usage examples

## 🔮 Roadmap

### Immediate Improvements
- [ ] GPT-4 Vision for visual element analysis
- [ ] Multi-language support for international sites
- [ ] Mobile device emulation for responsive testing
- [ ] Session-based testing with state preservation

### Long-term Goals
- [ ] A/B testing capabilities
- [ ] Machine learning for improved pattern recognition
- [ ] API integration for external services
- [ ] Plugin architecture for extensions
- [ ] Visual regression testing
- [ ] Integration with popular CI/CD platforms

---

**Made with ❤️ by the LangTest team** 