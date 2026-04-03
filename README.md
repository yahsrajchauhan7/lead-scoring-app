# Explainable Lead Scoring + Smart Outreach Assistant

🔗 Live Demo: https://lead-scoring-app-dcyw9wbvycv4l9fzmgqxnp.streamlit.app
📁 GitHub Repo: https://github.com/yahsrajchauhan7/lead-scoring-app

---

## Overview

Most lead generation tools focus on collecting a lot of data, but they don’t really help answer simple questions:

* Which leads should I focus on first?
* Why is this lead important?
* What should I do next?

I built this project to solve that problem. Instead of just showing data, this tool helps prioritize leads, explains the reasoning behind each score, and suggests what action to take.

---

## What it does

* Scores leads based on industry, location, contact details, and revenue
* Lets you adjust weights depending on your business goal
* Explains *why* a lead is valuable (not just a number)
* Suggests what to do next (e.g., reach out, review, ignore)
* Generates a simple outreach message
* Allows CSV upload and download

---

## How it works

Each lead is evaluated based on a few practical signals:

* Industry + location → how relevant the lead is
* Contact info → how easy it is to reach them
* Data completeness → how reliable the data is
* Revenue → potential business value

These are combined into a final score, which is then used to:

* Rank leads
* Assign priority (High / Medium / Low)
* Explain the score
* Suggest next steps

---

## Why I built this

From my perspective, the biggest gap in most lead tools is not data collection — it’s decision-making.

Sales teams still spend a lot of time manually reviewing leads. I wanted to build something simple that reduces that effort and makes the process more actionable.

---

## Trade-offs

Since this was built within a limited time:

* I used rule-based scoring instead of machine learning
* No external APIs are used for data enrichment
* Outreach messages are simple templates

---

## What I would improve next

* Add enrichment APIs (e.g., company data, emails)
* Use ML for smarter scoring
* Connect with CRM tools like HubSpot
* Improve UI design

---

## How to run

pip install -r requirements.txt
streamlit run app.py
