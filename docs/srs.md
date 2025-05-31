# 📋 Software Requirements Specification (SRS)

## Project: Investment Tracking & Strategy Automation System

**Version:** 1.0
**Author:** Omar Rodrigues
**Date:** 2025-05-12

---

## 1. Purpose

To build a production-grade application that:

* Tracks investments (stocks, ETFs, etc.)
* Applies automated strategies (e.g. alerts and sell signals)
* Ingests and analyzes live market data
* Uses real ML/statistical methods (not just LLMs)
* Minimizes required user interaction

---

## 2. Scope

This software will:

* Let users define and track their stock holdings
* Monitor live market prices
* Trigger alerts/sell logic based on thresholds
* Optionally automate trades (e.g. via Alpaca API)
* Apply machine learning for insights or strategy refinement

---

## 3. System Overview

| Component                   | Purpose                                                                |
| --------------------------- | ---------------------------------------------------------------------- |
| **Data Ingestion Module**   | Fetches live stock prices via API (Alpaca, Yahoo Finance, etc.)        |
| **Portfolio Tracker**       | Stores user holdings, entry price, quantity, and current market value  |
| **Alert Engine**            | Sends notices when stocks hit thresholds (e.g. -7% drop)               |
| **Sell Logic Module**       | Applies automatic actions (e.g. flag for sale, trigger API call)       |
| **ML Engine (later phase)** | Evaluates patterns or trends, can be trained for signal prediction     |
| **Web Interface or CLI**    | (Optional) View portfolio, manually add/remove assets, configure rules |
| **Persistent Storage**      | PostgreSQL or SQLite for local dev                                     |

---

## 4. Functional Requirements

### 4.1 Portfolio Management

* FR1. Users can add, update, or remove investments
* FR2. Each investment contains:

  * Ticker
  * Entry price
  * Quantity
  * Entry date
  * Optional alert thresholds

### 4.2 Live Data Ingestion

* FR3. The system fetches prices via scheduled job or on-demand
* FR4. Prices are persisted with timestamps for future analysis

### 4.3 Alerting & Sell Logic

* FR5. Alerts are triggered if current price drops by X% or hits target
* FR6. The system can flag investments for sale or call a sell function

### 4.4 Machine Learning (ML)

* FR7. The system allows model training from past price data (optional)
* FR8. Models can suggest strategy tuning or detect anomalies

---

## 5. Non-Functional Requirements

* **Performance:** System should support at least 500 tracked assets with sub-1s alert checks.
* **Reliability:** Background jobs must fail gracefully with error logging.
* **Maintainability:** Modular folder structure; all components isolated.
* **Security:** API keys (e.g. Alpaca, OpenAI) loaded via `.env`; no hardcoded secrets.
* **Portability:** Fully Dockerized, with CI/CD pipeline and support for local and cloud deployment.

---

## 6. Tech Stack

| Layer                | Tools                                   |
| -------------------- | --------------------------------------- |
| Programming Language | Python 3.11+                            |
| Data Fetching        | `alpaca-trade-api`, `yfinance`          |
| ML Libraries         | `scikit-learn`, `pandas`, `numpy`       |
| Backend Framework    | `FastAPI` (optional, for API/alerts UI) |
| Storage              | PostgreSQL (prod), SQLite (dev)         |
| Scheduler            | `APScheduler`                           |
| CI/CD                | GitHub Actions                          |
| Containerization     | Docker, Docker Compose                  |

---

## 7. Assumptions

* User has basic understanding of their investment strategy
* Project may later support multiple users, but is single-user for MVP
* The system will not execute trades without explicit user opt-in
