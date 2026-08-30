<h1 align="center">🐍 Python for SOC & Security Automation</h1>
<h3 align="center">A curated learning path, just what actually moves the needle for SOC work</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Focus-Scripting%20%26%20Automation-1E293B?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Relearning%20from%20Scratch-334155?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Goal-SOC%20Tooling%20%26%20Analysis-475569?style=for-the-badge"/>
</p>

---

## 🎯 Why this doc exists

I am currently engaged in a process of re-education in Python through a comprehensive general-purpose course that addresses various aspects of scripting and automation pertinent to the field of cybersecurity. This document specifically distills the course content to highlight the most essential components relevant to work within a Security Operations Center (SOC).

---

## 🎯 Priority Skills for SOC Work

Everything below is ranked by how directly it applies to SOC/security automation, not by course order. **Core** means non-negotiable, learn-it-now. **Applied** means genuinely useful, but sequenced in once the core is solid rather than day one.

| Tool | Tier | Why it matters here |
|---|---|---|
| **Python 3** | Core | The language itself: everything else builds on this |
| **Bash Command Line** | Core | Nearly every SOC/Linux task involves shell scripting alongside Python: log filtering, cron jobs, chaining tools |
| **Requests** | Core | The backbone of interacting with security APIs — VirusTotal, AbuseIPDB, Shodan, internal SIEM APIs — the single most directly applicable library for SOC automation |
| **Pandas** | Core | Log analysis at scale: filtering, aggregating, and pivoting CSV/JSON exports from Elasticsearch is exactly what Pandas is built for |
| **SQL / SQLite / PostgreSQL** | Core | Querying structured security data directly, and understanding the query language underneath tools like Kibana's Discover/ES|QL |
| **Python Scripting & Automation** | Core | The actual skill this whole course exists to build: task automation, file parsing, repetitive triage steps |
| **Beautiful Soup** | Applied | OSINT/threat intel gathering, scraping public breach-notification sites, IOC feeds |
| **Jupyter Notebook** | Applied | Exploratory log analysis, documenting data work step-by-step pairs naturally with Pandas |
| **Matplotlib / Seaborn** | Applied | Visualizing security data trend charts, anomaly spikes supplementary to what Kibana already does |
| **Scikit-learn** | Applied | Longer-term: basic anomaly detection or classification (e.g., flagging outlier login patterns) |
| **Flask + REST + APIs** | Applied | Small internal tools: a webhook receiver for alerts, a lightweight dashboard, a simple automation trigger |
| **PyCharm** | Applied | Primary IDE once scripts get past trivial size; debugging tools matter more as complexity grows |

---

## 🗂️ Python Projects

This doc stays focused on strategy: what to learn and why. The actual scripts and tools I build with these skills live in their own dedicated repo, documented as real, working projects rather than tutorial exercises.

📁 **[Python Security Projects](./python-security-projects/)** Every script/tool built as part of this learning path, documented with purpose, approach, and what it taught me.

---

## 🗺️ Learning Order (My Actual Plan)

1. **Python 3 fundamentals**: Syntax, data structures, functions, file I/O
2. **Bash + Git/GitHub in parallel**: These aren't "after Python"; they're alongside it from day one
3. **Requests**: start hitting real APIs early (VirusTotal's free tier is a good first target) to keep things grounded in actual SOC use cases, not abstract exercises
4. **Pandas**: Once comfortable with core Python, move into log/data manipulation
5. **SQL**: In parallel with Pandas, since both are about querying/shaping data
6. **Jupyter**: Once I have real scripts worth documenting and iterating on visually
7. **Everything in the "Supporting" tier**: Picked up as specific projects actually demand them, not in a fixed order

---

## 🔧 First Practical Project Ideas

Concrete, not abstract things I can actually build against my own SOC lab:
- A script that queries VirusTotal's API for a list of IOCs pulled from an incident write-up, and outputs a clean summary
- A Pandas script that ingests an exported CSV from Kibana (e.g., blocked pfSense traffic) and summarizes top source IPs / most-triggered rules
- A small script that checks whether a given IP appears in my own Elasticsearch indices, across all data streams, using the Requests + Elasticsearch REST API directly (bypassing Kibana's UI)

---

<p align="center"><i>Part of the SOC Home Lab documentation series, a living doc, updated as priorities shift with actual project needs.</i></p>
