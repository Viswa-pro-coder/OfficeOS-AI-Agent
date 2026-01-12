# 🏢 OfficeOS: The Secure, Unified Enterprise AI Platform

> **Project Day Demo** | A modular AI orchestration system designed to replace fragmented office tools with a single, secure interface.

---

## 📖 Executive Summary
In the modern enterprise, employees lose hours daily switching between disparate productivity tools. Furthermore, the rise of Generative AI has introduced a critical security vulnerability: "Shadow AI," where sensitive corporate data is pasted into public tools.

**OfficeOS** is a centralized, secure AI hub designed to unify these workflows. It replaces reliance on multiple external subscriptions with a modular "hub-and-spoke" architecture, where specific AI agents—ranging from Market Research to Legal Analysis—operate under strict company governance.

### 🔐 Key Value Propositions
* **Self-Hosted Ready:** Designed to work with local LLMs (like Llama 3) to ensure data never leaves the company server.
* **Unified Workflow:** Consolidates 8 distinct departments (Marketing, Legal, HR, etc.) into one dashboard.
* **Granular Auditing:** Tracks usage metrics per user/department for ROI analysis.

---

## 🤖 Functional Modules (The Agents)

OfficeOS consists of eight specialized AI Agents, each designed to automate a specific high-friction corporate task:

| Department | Module Name | Function |
| :--- | :--- | :--- |
| **Marketing** | 📈 **Market Researcher** | Scans live internet for real-time trends and competitor news. |
| **Admin** | 📧 **Email Auto-Drafter** | Analyzes sentiment and drafts professional email replies instantly. |
| **Operations** | 📝 **Meeting Minutes** | Transcribes messy notes into structured minutes with Action Items. |
| **HR** | 📄 **Resume Screener** | Scores candidates against job descriptions to filter talent faster. |
| **Content** | 📱 **Social Media Engine** | Converts dry announcements into viral LinkedIn/Twitter posts. |
| **Legal** | ⚖️ **Contract Simplifier** | Translates "Legalese" into plain English and flags risk factors. |
| **IT** | 🐛 **Code Bug Hunter** | Analyzes code, finds bugs, and provides fixed code blocks. |
| **Finance** | 🧹 **Data Cleaner** | Converts unstructured text data into clean CSV tables for Excel. |

---

## ⚙️ Installation & Setup

Follow these steps to deploy OfficeOS on your local machine.

### 1. Clone the Repository
```bash
git clone [https://github.com/Viswa-pro-coder/OfficeOS-AI-Agent.git](https://github.com/Viswa-pro-coder/OfficeOS-AI-Agent.git)
cd OfficeOS-AI-Agent
```
### 2. Install Dependencies
```bash

pip install -r requirements.txt
```
### 3. Configure API Keys (The Vault)
```bash
Since this project simulates a secure environment, you must provide your own API keys.

Create a folder named .streamlit in the root directory.

Inside it, create a file named secrets.toml.

Add your keys (Groq for Intelligence, Serper for Search):

Ini, TOML

# .streamlit/secrets.toml
GROQ_API_KEY = "gsk_..."
SERPER_API_KEY = "..."
```
### 4. Run the Application
```bash


streamlit run app.py
```
🛠️ Tech Stack
Frontend: Streamlit (Python-based UI)

Orchestration: LangChain

Intelligence: Groq API (Llama 3.3 70B Model)

Search Tool: SerperDev (Google Search API)

Built for Project Day Presentation. Not for production use without proper security hardening.


***

### 🚀 Final Polish
Once you commit this file, go back to your repository's main page. You will see this beautiful documentation rendered with tables and headings right below your code files.

You are officially done! You have:
1.  **A working product** (8 real AI agents).
2.  **A secure codebase** (Keys hidden).
3.  **Professional Documentation** (Executive summary + Tech guide).

**Good luck on Project Day! You are going to crush it.**
