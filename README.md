# 🚀 API & UI Automation Testing Framework
This repository contains an integrated automated testing framework for API Testing (Reqres.in) and UI Testing (SauceDemo).
The framework utilizes industry standards such as the Page Object Model (POM) for UI and Dynamic Mocking for API stability.

---

## 📋 Test Coverage

1. **API Testing (Reqres.in - 33 Test Cases)**
Testing the List Users endpoint with various scenarios:
Positive Cases: Validation of HTTP 200 status, JSON structure, data accuracy, and data type formatting.
Negative Cases: Handling of invalid page parameters (strings, special characters, negative numbers, zero, and null).
Edge & Boundary: Validation of optional fields, SLA response time (< 2s), server error simulations (500/408), and page limit boundaries.

2. **UI Testing (SauceDemo - 16 Test Cases)**
Comprehensive end-to-end testing using the Page Object Model (POM):
Positive Cases (TC-UI-001 - 010): Successful login, dashboard element validation (headers, product list, cart icon), product sorting (A-Z, Z-A, Price Low-High), and Logout functionality.
Negative Cases (TC-UI-011 - 016): Login with incorrect passwords, non-existent users, empty fields (null), and locked-out account validation.

---

## 🛠️ Prerequisites

Ensure you have the following installed:
* [Python 3.11+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads)

---

## 🚀 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ahsinf/api-ui-automation.git
   cd qa-assignment-test
   ```
2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate     # For Windows
   ```
3. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Install Playwright Browsers**
   This command downloads the browser binaries (Chromium, Firefox, WebKit) that Playwright uses.
   ```bash
   playwright install
   ```

## 🏃 Running the Tests
🔹 API Automation (Reqres.in)
1. **Execute tests in the terminal:**
   ```bash
   pytest tests/api/test_reqres_api.py -v
   ```
2. **Generate a Visual HTML Report:**
   ```bash
   pytest tests/api/test_reqres_api.py --html=report_api.html --self-contained-html
   ```

🔹 UI Automation (SauceDemo)
1. **Run UI tests with video recording and screenshot features:**
   ```bash
   # Run tests in Headless mode (browser hidden)
   python -m pytest -v tests/ui/test_sauce_demo.py --video on --html=report_ui.html --self-contained-html

   # Run tests in Headed mode (browser visible)
   python -m pytest -v tests/ui/test_sauce_demo.py --headed
   ```

## 🎁 Bonus Assignment: Data Generation
This script generates a CSV report (`user_data_report.csv`) from the Reqres Page 2 dataset.

**Technical Implementation:**
To ensure reliability against live server instability or Cloudflare WAF blocking (403 Forbidden), the script uses a **Fallback Architecture**. It attempts a live API fetch first; if the server is unreachable or blocks the request, it automatically utilizes a validated internal dataset to guarantee the report is generated correctly.

**To run:**
```bash
python generate_user_data.py
```

## 📊 Reporting
The framework provi
HTML Reports: Interactive reports (report_api.html & report_ui.html) featuring success rate charts, test durations, and failure details.
Screenshots: Automated screen capture during UI execution, embedded directly into the HTML report.
Video Recordings: Full execution videos saved in the test-results/ directory (enabled via --video on).
API Response Logs: JSON response bodies printed to the terminal for audit purposes (enabled via -s).

## 💡 Framework Key Features
- Dynamic Mocking: Uses requests-mock callbacks to simulate various server conditions locally. This bypasses Cloudflare bot protection (Error 403) and ensures ultra-fast, stable execution.
- Page Object Model (POM): Separates test logic from UI selectors, ensuring high maintainability and reduced code duplication.