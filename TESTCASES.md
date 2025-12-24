# Test Cases for Avito QA Internship Assignment

## Overview
This document outlines the test cases for the Microservice API.
Host: `https://qa-internship.avito.com`

## Endpoints
1.  **Create Advertisement**: `POST /api/1/item`
2.  **Get Advertisement by ID**: `GET /api/1/item/:id`
3.  **Get Advertisements by Seller ID**: `GET /api/1/:sellerID/item`
4.  **Get Statistics by Item ID**: `GET /api/1/statistic/:id`

## Test Cases

### 1. Create Advertisement
**TC-001: Create a valid advertisement**
*   **Description**: Verify that a user can create an advertisement with valid data.
*   **Pre-conditions**: None.
*   **Steps**:
    1.  Generate a random `sellerID` (111111-999999).
    2.  Send `POST /api/1/item` with valid JSON body (name, price, statistics).
*   **Expected Result**:
    *   Status Code: 200 OK.
    *   Response body contains a unique `id` for the created item.
    *   Response body matches the sent data (sellerId, name, price, statistics).

**TC-002: Create advertisement with missing required fields**
*   **Description**: Verify that the system rejects requests with missing required fields.
*   **Steps**:
    1.  Send `POST /api/1/item` with missing `name` or `price`.
*   **Expected Result**:
    *   Status Code: 400 Bad Request.

**TC-003: Create advertisement with invalid data types**
*   **Description**: Verify that the system rejects requests with invalid data types.
*   **Steps**:
    1.  Send `POST /api/1/item` with string `price` (where integer is expected) or invalid `statistics`.
*   **Expected Result**:
    *   Status Code: 400 Bad Request.

### 2. Get Advertisement by ID
**TC-004: Get existing advertisement by ID**
*   **Description**: Verify that a user can retrieve a created advertisement by its ID.
*   **Pre-conditions**: An advertisement exists (create one first).
*   **Steps**:
    1.  Create a new advertisement and get its `id`.
    2.  Send `GET /api/1/item/{id}`.
*   **Expected Result**:
    *   Status Code: 200 OK.
    *   Response body matches the created advertisement details.

**TC-005: Get non-existent advertisement by ID**
*   **Description**: Verify system behavior when requesting a non-existent ID.
*   **Steps**:
    1.  Send `GET /api/1/item/{non_existent_id}` (e.g., a random UUID or invalid format).
*   **Expected Result**:
    *   Status Code: 404 Not Found.

### 3. Get Advertisements by Seller ID
**TC-006: Get all advertisements for a seller**
*   **Description**: Verify that a user can retrieve all advertisements for a specific seller.
*   **Pre-conditions**: Create multiple advertisements for the same `sellerID`.
*   **Steps**:
    1.  Generate a unique `sellerID`.
    2.  Create 2-3 advertisements with this `sellerID`.
    3.  Send `GET /api/1/{sellerID}/item`.
*   **Expected Result**:
    *   Status Code: 200 OK.
    *   Response body is an array containing all created advertisements for that seller.

**TC-007: Get advertisements for non-existent seller**
*   **Description**: Verify system behavior when requesting items for a seller with no advertisements.
*   **Steps**:
    1.  Generate a random `sellerID` that hasn't been used.
    2.  Send `GET /api/1/{sellerID}/item`.
*   **Expected Result**:
    *   Status Code: 200 OK.
    *   Response body is an empty array `[]`.

### 4. Get Statistics by Item ID
**TC-008: Get statistics for an existing item**
*   **Description**: Verify that a user can retrieve statistics for an item.
*   **Pre-conditions**: An advertisement exists.
*   **Steps**:
    1.  Create a new advertisement and get its `id`.
    2.  Send `GET /api/1/statistic/{id}`.
*   **Expected Result**:
    *   Status Code: 200 OK.
    *   Response body contains the statistics object (likes, viewCount, contacts).

**TC-009: Get statistics for non-existent item**
*   **Description**: Verify system behavior when requesting statistics for a non-existent item.
*   **Steps**:
    1.  Send `GET /api/1/statistic/{non_existent_id}`.
*   **Expected Result**:
    *   Status Code: 404 Not Found.
