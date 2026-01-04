# 🚀 Reqres.in API Automation Testing Framework

[![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-pytest-red.svg)](https://docs.pytest.org/)
[![Mocking](https://img.shields.io/badge/library-requests--mock-orange.svg)](https://requests-mock.readthedocs.io/)

A comprehensive API automation testing suite designed for the **List Users** endpoint at [Reqres.in](https://reqres.in/). This project implements 33 manual test cases into a robust automation framework, covering positive, negative, edge, and boundary scenarios.

---

## 📋 Test Coverage (33 Test Cases)

The test suite is categorized based on standard QA methodologies:

### 1. Positive Cases (TC-API-001 - 010)
* **Validation:** HTTP Status Code 200 OK.
* **Response Structure:** Verified existence of key fields (`page`, `per_page`, `data`, etc.).
* **Data Accuracy:** Verified page values match request parameters.
* **Data Format:** Ensured numeric IDs, valid Email formats, and Avatar URL strings.

### 2. Negative Cases (TC-API-011 - 021)
* **Input Handling:** Verified graceful handling of invalid `page` parameters (Strings, Special Characters, Negative Numbers, Zero, and Null).
* **Data Integrity:** Validated that returned data is not null and maintains correct data types even under stress.

### 3. Edge Cases (TC-API-022 - 028)
* **Optional Fields:** Ensured `last_name` and `avatar` keys exist in the structure (even if values are empty).
* **Performance:** Validated Response Time is within SLA (< 2 seconds).
* **Robustness:** Verified API ignores unexpected additional query fields.
* **Error Handling:** Simulated server-side failures (408 Timeout & 500 Internal Server Error).

### 4. Boundary Cases (TC-API-029 - 033)
* **Pagination Limits:** Validated behavior at minimum (Page 1) and maximum valid data pages.
* **Out-of-Bounds:** Ensured empty data arrays are returned when requesting non-existent pages (e.g., Page 999).

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

## 🏃 Running the Tests
1. **Execute tests in the terminal:**
   ```bash
   pytest tests/api/test_reqres_api.py -v
   ```
2. **Generate a Visual HTML Report:**
   ```bash
   pytest tests/api/test_reqres_api.py --html=report_api.html --self-contained-html
   ```

## 📊 Reporting
The project utilizes pytest-html to create professional visual reports.
- After execution, open report_api.html in your browser (Chrome/Safari).
- Key Report Features:
  - Success Rate Pie Chart.
  - Detailed status per Test Case ID.
  - Custom descriptive error messages for any failed assertions.

## 💡 Framework Key Features
Dynamic Mocking: Uses requests-mock callbacks to simulate various server conditions locally. This bypasses Cloudflare bot protection (Error 403) and ensures ultra-fast, stable execution.