# 💼 Multi-Agent Financial Advisor System
## 📌 Project Title
**Multi-Agent AI Financial Advisor for Investing, Tax Optimization & Retirement Planning**

## 📖 Project Overview

This project is a **production-ready multi-agent AI financial advisory system** designed to deliver **holistic, personalized financial guidance**.  
It integrates **investment advisory**, **tax optimization**, and **retirement planning** into a unified intelligent platform.

The system leverages:
- **Specialized AI agents** coordinated by an Orchestrator Agent
- **Real-time market intelligence**
- **Advanced Retrieval-Augmented Generation (RAG)** with hybrid search
- **Structured financial data pipelines**
- **Educational visual generation using OpenAI Images**

The advisor interprets a user’s **full financial profile** (income, assets, liabilities, goals, risk tolerance) and produces **coherent, actionable financial plans** while resolving conflicts between investment growth, tax efficiency, and long-term retirement objectives.

---

## 🎯 Key Objectives

-Deliver personalized financial advice based on user profiles
-Simulate real-world advisor collaboration
-Combine static financial knowledge with live market data
-Ensure explainability, structure, and auditability of AI outputs
-Enable scalable, multi-user financial analysis

## ✨ Key Features

- 🧠 **Multi-Agent Architecture**
  - Investment Advisor Agent
  - Tax Consultant Agent
  - Retirement Planner Agent
  - Orchestrator Agent for routing & conflict resolution

- 📊 **Portfolio Analysis & Optimization**
  - Asset allocation recommendations
  - Risk/return optimization (Modern Portfolio Theory)
  - Rebalancing strategies
  - Scenario & stress testing

- 💰 **Tax Optimization Intelligence**
  - Capital gains optimization
  - Tax-advantaged account strategies 
  - Jurisdiction-aware tax advice (CA|US)

- 🏖️ **Retirement Planning**
  - Long-term contribution strategies
  - Retirement timelines & projections
  - Account selection & withdrawal planning

- 🔎 **Advanced RAG (Retrieval-Augmented Generation)**
  - Hybrid search (vector + keyword)
  - Metadata filters (jurisdiction, asset class, account type)
  - Structured JSON-based knowledge ingestion

- 🎨 **Educational Visual Generation**
  - Portfolio allocation diagrams
  - Retirement timelines
  - Diversification illustrations
  - Financial concept graphics (risk vs return, compounding)


- ⚡ **Live Market & Web Intelligence**
  - Real-time market prices
  - Live financial news & macro context

## 🛠️ Tools Used by the Multi-Agent System

| Tool | Purpose |
|---|---|
| `rag_search_tool` | Retrieval from curated financial knowledge base |
| `perplexity_live_search` | Live web & market intelligence |
| `calculate_weights` | Portfolio weight optimization |
| `calculate_volatility_correlation` | Risk & correlation analysis |
| `portfolio_analysis` | Performance, diversification & scenario analysis |
| `Yahoo_market_prices` | Live & historical market data |
| `analyze_tax_scenario` | Tax impact simulations & optimization |

---

## 📁 Data Collection & Curation Process

The platform uses a **structured, JSON-first data pipeline** to enable advanced RAG capabilities.

### 🔹 Data Sources
- Financial education sources (PersonalFinance_v2)
- Market data APIs (Yahoo Finance)
- User-provided financial profiles (CSV → JSON)

### 🔹 Processing Pipeline
1. **Data ingestion** (PersonalFinance_v2 Jsonl, CSVs)
2. **Chunking & semantic segmentation**
3. **Normalization into structured JSON**
4. **Metadata enrichment**
   - Category
   - Topics
   - jurisdiction
   - Title
   - Source
5. **Vector embedding & indexing**
6. **Hybrid search (semantic + keyword)**

### 🔹 Why Structured JSON?
- Enables **fine-grained metadata filtering**
- Improves **retrieval accuracy**
- Allows **agent-specific context injection**
- Supports **explainability & traceability**

---

## 🔎 RAG Pipeline: Hybrid Search with Metadata Filters

The system uses a **hybrid retrieval strategy**:
- **Dense vector search** for semantic understanding
- **Sparse keyword search** for precision
- **Metadata filters** for constraints such as:
  - Country (US / Canada)
  - Category
   - Topics
   - jurisdiction
   - Title
   - Source

This ensures **highly relevant, compliant, and explainable responses**.

---

## 🖼️ OpenAI Image Generation

The application integrates **OpenAI Images** to generate educational and explanatory visuals, including:

- 📊 Portfolio allocation diagrams
- 🕒 Retirement timelines
- 🌍 Diversification illustrations
- 📈 Financial concept graphics:
  - Risk vs return
  - Compounding growth
  - Asset correlation

These visuals enhance **user understanding** and **financial literacy**.

---

## 💸 Cost of Using the Application

### 🔹 AI Models Used

| Component | Model | Cost Consideration |
|---|---|---|
| Core reasoning & agents | `gpt-4.1` | Higher reasoning quality, premium pricing |
| Live web search | `sonar-pro` (Perplexity) | Pay-per-query |
| Image generation | OpenAI Images API | Per image generated |
| Embeddings (RAG) | OpenAI embeddings | One-time + incremental |

### 🔹 Estimated Cost Drivers
- Number of user queries
- Depth of reasoning (token usage)
- Frequency of live web searches
- Volume of generated images
- Size of RAG corpus

> **Typical usage**:  
> - Text-based advisory: low to moderate cost per session  
> - Sessions with live search + images: moderate cost  
> - Heavy portfolio simulations & visuals: higher cost


## 🚀 Summary

This project delivers a **scalable, explainable, and intelligent financial advisor** by combining:
- Multi-agent orchestration
- Advanced RAG with hybrid search
- Real-time market intelligence
- Structured financial knowledge
- AI-generated educational visuals

It is designed for **modern fintech applications**, wealth management platforms, and AI-powered financial planning solutions.

--- 

## ⚠️ Risk Disclaimer & Important Notice

This application is provided **for educational and informational purposes only** and **does not constitute financial, investment, tax, or legal advice**.

### Key Disclaimers

- 📉 **Investment Risk**  
  All investments involve risk, including the possible loss of principal. Past performance is not indicative of future results. Market conditions, economic factors, and individual circumstances can change rapidly.

- 🧾 **No Personalized Financial Advice**  
  While the system generates personalized insights based on user-provided data, it does **not replace a licensed financial advisor, tax professional, or legal consultant**.

- 🌍 **Jurisdictional Limitations**  
  Tax and retirement guidance is based on generalized interpretations of publicly available regulations (e.g., IRS, CRA). Laws and regulations vary by jurisdiction and may change without notice.

- 🤖 **AI-Generated Content**  
  Outputs are generated by AI models and external data sources. Despite safeguards and structured retrieval, responses **may contain inaccuracies, omissions, or outdated information**.

- 🔍 **User Responsibility**  
  Users are solely responsible for:
  - Verifying information independently
  - Making final financial decisions
  - Consulting qualified professionals before acting on recommendations

- 📊 **Scenario & Projection Assumptions**  
  Retirement projections, portfolio simulations, and tax scenarios rely on assumptions (e.g., growth rates, inflation, tax laws) that may not reflect future realities.

  ---

## 🚀 Quick Start

Follow these steps to get the Multi-Agent AI Financial Advisor up and running locally.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/CheunAnthony/financial_advisor.git
cd financial_advisor

2️⃣ Setup Environment Variables

Create your environment file and add your API keys:
mv .env.example .env

3️⃣ Install Dependencies

This project uses uv for fast and reproducible dependency management.

uv sync

4️⃣ Select Jupyter Kernel

If you are running notebooks (.ipynb files):

Open any .ipynb file

Click “Select Kernel” in the top-right corner of your IDE

Choose Python Environments

Select the .venv interpreter created by uv


