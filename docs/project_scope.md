# 📈 Investment Tracking System - MVP + Core Features

This document outlines the initial Minimum Viable Product (MVP) scope and essential features for the investment tracking system. The system combines portfolio management, alert logic, automated strategies, and statistical/ML tools to support both passive and active investors.

---

## 🧩 MVP + Core Feature Set

### 1. 🧾 Portfolio Tracker (Core)

* **Function**: Store and manage user investment positions (ticker, shares, cost basis, date).
* **Purpose**: Base layer for all downstream logic (e.g., alerts, automated trades).
* **Justification**: Foundational data structure for investment tracking.

### 2. 📡 Live Data Ingestion Module

* **Function**: Fetch real-time or near-real-time stock prices via Alpaca, Yahoo Finance, or Polygon.
* **Purpose**: Enables accurate valuation, alert evaluation, and automated decisions.
* **Justification**: Critical to power all real-time logic.

### 3. 🔔 Threshold-Based Alerts

* **Function**: Users configure alert rules (e.g., price drop >7%, specific price targets).
* **Purpose**: Notify users of critical changes in holding value.
* **Justification**: Enables passive monitoring, a key utility of the system.

### 4. ⚙️ Auto-Sell Signal Logic

* **Function**: Configurable rules to simulate or trigger "sell" actions on threshold breach.
* **Purpose**: Strategy enforcement and risk management.
* **Justification**: Core feature for users seeking automated defensive behavior.

### 5. 📬 Push Notifications

* **Function**: Optional email/SMS alerts for triggers (Twilio, SendGrid).
* **Purpose**: Deliver actionable information immediately.
* **Justification**: Improves responsiveness and real-world utility.

### 6. 🧠 ML/Statistical Engine

* **Function**: Use statistical models or machine learning to:

  * Identify abnormal patterns (anomaly detection)
  * Predict short-term directional risk
  * Score stock risk or opportunity levels
* **Purpose**: Enhance decision-making with data-driven signals.
* **Justification**: Moves system beyond rule-based logic into predictive capability.

### 7. 🧪 Backtesting Engine

* **Function**: Simulate trade signals and strategies against historical market data.
* **Tools**: QuantConnect (C#/Python) or Backtrader (Python).
* **Purpose**: Validate performance of alert rules and ML models.
* **Justification**: Reduces risk and increases confidence in strategy.

### 8. 🖥️ Minimal Interface (CLI or Web UI)

* **Function**: Input holdings, configure alerts, view logs.
* **Tools**: Typer/FastAPI (CLI + REST), or Streamlit/Next.js for web UI.
* **Purpose**: Provide minimal friction access to core features.
* **Justification**: Needed for user interaction.

### 9. 🧱 Persistent Storage Layer

* **Function**: Store user config, portfolio data, alert logs.
* **Tech**: SQLite (local dev), PostgreSQL (prod-ready).
* **Justification**: Enables recovery, querying, and future analytics.

---

## 🧠 Design Goals

* Real statistical/ML methods (not only LLM-based)
* Useful without daily interaction
* Automated alerting and optional execution
* Extensible and modular

---

## 🛠️ Initial Tools & Stack

* **Language**: Python
* **Live Data**: Alpaca, Yahoo Finance API, or Polygon.io
* **Backtesting**: Backtrader or QuantConnect
* **ML/Stats**: Scikit-learn, Prophet, or custom models
* **Storage**: SQLite → PostgreSQL
* **Interface**: CLI (Typer) or FastAPI
* **Deployment-ready via**: Docker + GitHub CI

---

This scope will evolve, but all major components above will be included in the first working version of the app.
