<h1 align="center">🐍 Python for SOC & Security Automation</h1>
<h3 align="center">A curated learning path — not everything in the course, just what actually moves the needle for SOC work</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Focus-Scripting%20%26%20Automation-1E293B?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Relearning%20from%20Scratch-334155?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Goal-SOC%20Tooling%20%26%20Analysis-475569?style=for-the-badge"/>
</p>

---

## 🎯 Why this doc exists

I'm relearning Python from scratch through a broad general-purpose course — covering everything from game development to web design to deployment. Most of it is genuinely useful for *someone*, but not all of it is useful for *this* goal: getting better at scripting and automation for cybersecurity work. This doc is my own filter — what to prioritize, what supports the priority, and what to consciously deprioritize for now, so I don't spread myself across 30 tools when 10 would actually make me dangerous in a SOC context.

---

## 🥇 Priority — Core to SOC Work

These are the tools I'm treating as non-negotiable, directly tied to real SOC/security automation tasks.

| Tool | Why it matters here |
|---|---|
| **Python 3** | The language itself — everything else builds on this |
| **Bash Command Line** | Nearly every SOC/Linux task involves shell scripting alongside Python — log filtering, cron jobs, chaining tools |
| **Git, GitHub & Version Control** | Every script I write should be tracked, documented, and reusable — this is also how this whole lab documentation practice already works |
| **Requests** | The backbone of interacting with security APIs — VirusTotal, AbuseIPDB, Shodan, internal SIEM APIs — this is the single most directly-applicable library for SOC automation |
| **Pandas** | Log analysis at scale — filtering, aggregating, and pivoting CSV/JSON exports from Elasticsearch or other tools is exactly what Pandas is built for |
| **SQL / SQLite / PostgreSQL** | Querying structured security data directly, and understanding the query language underneath tools like Kibana's discover/ES|QL |
| **Python Scripting & Automation (general)** | The actual skill this whole course exists to build — task automation, file parsing, repetitive triage steps |

---

## 🥈 Supporting — Useful, Secondary Priority

Valuable, but I'm treating these as "learn once the core is solid," not day-one priorities.

| Tool | Where it fits |
|---|---|
| **Beautiful Soup** | OSINT/threat intel gathering — scraping public breach-notification sites, threat actor forums (where legally/ethically accessible), IOC feeds |
| **Jupyter Notebook** | Ideal for exploratory log analysis and documenting an investigation's data work step-by-step — pairs naturally with Pandas |
| **Matplotlib / Seaborn** | Visualizing security data — trend charts, anomaly spikes — supplementary to what Kibana already does, but useful for custom analysis outside the SIEM |
| **Scikit-learn** | Longer-term: basic anomaly detection or classification (e.g. flagging outlier login patterns) — genuinely relevant to SOC work, just a later-stage skill once fundamentals are solid |
| **Flask + REST + APIs** | Building small internal tools — a webhook receiver for alerts, a lightweight dashboard, a simple automation trigger. Useful, not urgent |
| **PyCharm** | My primary IDE once scripts get past trivial size — good debugging tools matter more as complexity grows |

---

## 🗂️ Python Projects — Tracked Separately

Rather than list what I'm *not* focusing on, I'm tracking actual built projects in their own dedicated repo — same structure as my [SOC Incident Documentation](https://github.com/Tmitchy/-SOC-Incident-Documentation) repo: a master index, a reusable template, and each project as its own file. This keeps this learning-path doc focused on strategy, while the projects repo shows the actual work as it happens.

📁 **[Python Security Projects](./python-security-projects/)** — every script/tool built as part of this learning path, documented with purpose, approach, and what it taught me.

---

## 🗺️ Learning Order — My Actual Plan

1. **Python 3 fundamentals** — syntax, data structures, functions, file I/O
2. **Bash + Git/GitHub in parallel** — these aren't "after Python," they're alongside it from day one
3. **Requests** — start hitting real APIs early (VirusTotal's free tier is a good first target) to keep things grounded in actual SOC use cases, not abstract exercises
4. **Pandas** — once comfortable with core Python, move into log/data manipulation
5. **SQL** — in parallel with Pandas, since both are about querying/shaping data
6. **Jupyter** — once I have real scripts worth documenting and iterating on visually
7. **Everything in the "Supporting" tier** — picked up as specific projects actually demand them, not in a fixed order

---

## 🔧 First Practical Project Ideas

Concrete, not abstract — things I can actually build against my own SOC lab:
- A script that queries VirusTotal's API for a list of IOCs pulled from an incident write-up, and outputs a clean summary
- A Pandas script that ingests an exported CSV from Kibana (e.g. blocked pfSense traffic) and summarizes top source IPs / most-triggered rules
- A small script that checks whether a given IP appears in my own Elasticsearch indices, across all data streams, using the Requests + Elasticsearch REST API directly (bypassing Kibana's UI)

---

<p align="center"><i>Part of the SOC Home Lab documentation series — a living doc, updated as priorities shift with actual project needs.</i></p>
