# Avito QA Internship Assignment

This repository contains the automated test suite for the Avito QA Internship assignment.
The tests cover the Microservice API for managing advertisements.

## Project Structure
*   `TESTCASES.md`: Documentation of the test scenarios.
*   `test_api.py`: Automated tests using Python and pytest.
*   `debug_api.py`: Helper script for debugging API responses.
*   `README.md`: This file.

## Prerequisites
*   Python 3.x installed.
*   `pip` (Python package installer).

## Installation
1.  Install the required dependencies:
    ```bash
    pip install pytest requests
    ```
    *Note: If `pip` is not in your PATH, try `python -m pip install pytest requests` or `py -m pip install pytest requests`.*

## Running Tests
To execute the automated tests, run the following command:

```bash
pytest test_api.py
```

Or if using the Python launcher:
```bash
py -m pytest test_api.py
```

## Test Results
The tests will output the results in the console.
*   **Passed**: The feature is working as expected.
*   **Failed**: There is a discrepancy between expected and actual behavior.

## API Endpoints Tested
*   `POST /api/1/item` - Create Advertisement
*   `GET /api/1/item/:id` - Get Advertisement by ID
*   `GET /api/1/:sellerID/item` - Get Advertisements by Seller ID
*   `GET /api/1/statistic/:id` - Get Statistics by Item ID
