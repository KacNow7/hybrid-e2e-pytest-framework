# Hybrid E2E Test Automation Framework

A production-ready, highly scalable, and fully containerized End-to-End (E2E) testing framework that integrates user interface (UI) automation with backend API validation. This framework is designed to demonstrate advanced, mid-level software quality assurance engineering principles, moving away from brittle, script-based testing toward an enterprise-grade infrastructure.

The target system under test is the Restful-Booker platform, utilizing both its front-end web interface and its underlying REST API.

## Key Features

* **Page Object Model (POM) Architecture:** Complete isolation of UI locators and interaction logic from the actual test assertions, ensuring high maintainability and clean code.
* **Multi-Layer Validation (UI + API):** Combines fast API requests for state initialization and data setup with detailed Selenium WebDriver scripts for end-to-end user journey validation.
* **Advanced Fixture Lifecycle (Setup/Teardown):** Utilizes Pytest fixtures to dynamically prepare test environments (e.g., creating test bookings via API) and systematically clean up data after execution, guaranteeing test isolation.
* **Environment & Configuration Management:** Decouples configuration from code using `python-dotenv`. Supports seamless switching between different testing environments (QA, Dev, Prod) via command-line arguments.
* **Data-Driven & Dynamic Testing:** Implements test parameterization using `@pytest.mark.parametrize` alongside the `Faker` library to generate unique datasets, increasing test coverage without duplicating code.
* **Parallel Test Execution:** Configured with `pytest-xdist` to run tests concurrently across multiple CPU cores, drastically reducing execution times in continuous integration pipelines.
* **Full Containerization & Grid Execution:** Orchestrated with Docker and Docker Compose. Runs test suites inside an isolated Python container while routing UI commands to a scalable Selenium Standalone Chrome Grid container.
* **Live Test Observability (VNC):** Includes a built-in noVNC server inside the containerized Selenium environment, allowing real-time visual monitoring of headless browser interactions.
* **Automated Failure Capture:** Custom Pytest hooks automatically capture browser screenshots upon test failure and embed them directly into report artifacts.
* **Enterprise Reporting:** Integrated with Allure Report to generate comprehensive, interactive HTML reports featuring visual statistics, failure timelines, and embedded attachments.

## Project Structure

```text
hybrid-e2e-pytest-framework/
├── .devcontainer/         # Environment definition for cloud-based development
├── .github/               # Continuous Integration workflows
│   └── workflows/
│       └── python-tests.yml
├── pages/                 # Page Object Model layer
│   ├── base_page.py       # Core wrapper for Selenium explicit waits and actions
│   └── login_page.py      # Encapsulated locators and behaviors for the admin panel
├── tests/                 # Test suites and configuration
│   ├── conftest.py        # Global fixtures, driver initialization, and hooks
│   ├── test_api.py        # Backend REST API validation suites
│   └── test_hybrid.py     # Cross-layer UI and API integration scenarios
├── .env                   # Environment variables (local-only, ignored by Git)
├── .gitignore             # Git exclusion rules
├── Dockerfile             # Blueprint for the Python test runner container
├── docker-compose.yml     # Multi-container orchestration specification
├── requirements.txt       # Hardened dependency definitions
└── README.md              # Framework documentation
```

## Prerequisites

To execute this framework locally or within a containerized environment, ensure you have:
* Python 3.10 or higher (if running locally)
* Docker and Docker Compose (highly recommended for isolated execution)
* Google Chrome installed (if running local UI tests without Docker)

## Installation and Configuration

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/KacNow7/hybrid-e2e-pytest-framework.git](https://github.com/KacNow7/hybrid-e2e-pytest-framework.git)
   cd hybrid-e2e-pytest-framework
   ```

2. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   UI_BASE_URL=[https://automationintesting.online/](https://automationintesting.online/)
   API_BASE_URL=[https://restful-booker.herokuapp.com](https://restful-booker.herokuapp.com)
   ```

3. **Local setup (Optional):**
   If you prefer running tests outside of Docker, install the dependencies directly:
   ```bash
   pip install -r requirements.txt
   ```

## Execution Guide

### 1. Execution via Docker Compose (Recommended)
This approach requires no local dependencies other than Docker. It builds the test runner and provisions a headless Chrome browser alongside a live VNC stream.

```bash
# Build images and execute the entire suite
docker compose up --build
```

* **Live View Feature:** While the containerized tests are running, open your host browser and navigate to `http://localhost:7900`. Use the password `secret` to view the headless browser executing actions in real time via noVNC.
* **Cleanup:** Once execution finishes, tear down the infrastructure:
  ```bash
  docker compose down
  ```

### 2. Local Execution
To execute the tests locally across multiple threads using the installed Python interpreter:

```bash
# Run all tests concurrently across 2 workers
pytest -n 2 --alluredir=.allure_results
```

## Reporting

This framework uses Allure Report to compile test results. After executing tests with the `--alluredir=.allure_results` flag (automatic when using Docker), follow these steps to review the interactive dashboard:

1. **Install Allure Commandline** via your system package manager (e.g., `npm install -g allure-commandline` or `brew install allure`).
2. **Generate and open the report:**
   ```bash
   allure serve .allure_results
   ```

The resulting dashboard displays comprehensive status charts, parameterized test data tables, execution duration trends, and automated screenshots captured at the exact moment of any test failure.
