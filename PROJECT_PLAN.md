# 📌 Project Plan – OfficeGenie: Smart Workplace Helpdesk

OfficeGenie is a GenAI-powered assistant that triages natural language support queries from employees. It classifies issues (IT, HR, Admin, etc.), extracts key details, sends instant auto-responses, and routes them to the correct team or automation — all from a simple webform.

---

## 🗺️ High-Level Phases

| Phase | Description |
|-------|-------------|
| **1. Setup & Design**         | Define goals, UX flow, data schema, and prompt strategy |
| **2. Core MVP Development**   | Build input form, classification & extraction pipeline, auto-response logic |
| **3. Storage & Logging**      | Store input/output for dashboard and testing |
| **4. UI & Experience Polish** | Add response display, error handling, basic analytics |
| **5. Showcase Readiness**     | Prepare GitHub project, add documentation and a case study |

---

## ✅ Milestone Breakdown

### 🛠️ Milestone 1: Project Setup & Design
> ⏱️ Estimated: 1 day

- [ ] Define use cases and categories (IT, HR, Admin, etc.)
- [ ] Create sample input/output data
- [ ] Design prompt template for LLM classification and extraction

**Output:**
- `data/sample-user-input.json`
- `data/sample-system-output.json`
- `app/prompts.py`

---

### 💻 Milestone 2: Core LLM-Powered MVP
> ⏱️ Estimated: 2–3 days

- [ ] Build webform UI with Streamlit or Flask
- [ ] Capture full name, email, message, and department
- [ ] Create LLM pipeline to classify and extract structured output
- [ ] Generate auto-response based on prediction

**Output:**
- `app/main.py`
- `app/llm_pipeline.py`

---

### 🧾 Milestone 3: Storage + Logging
> ⏱️ Estimated: 1 day

- [ ] Store form inputs and model outputs to JSON/SQLite
- [ ] Capture user metadata + timestamps
- [ ] Enable simple log retrieval or export

**Output:**
- `data/tickets.db` or JSON logs
- `utils/storage.py`

---

### 📊 Milestone 4: Dashboard & Analytics (Basic)
> ⏱️ Estimated: 1–2 days

- [ ] Display ticket volume by category
- [ ] Show breakdown by department or urgency
- [ ] Visualize trends or query frequency

**Output:**
- `app/dashboard.py`

---

### 📚 Milestone 5: Packaging & Showcase
> ⏱️ Estimated: 1 day

- [ ] Finalize `README.md` with screenshots, setup, features
- [ ] Write technical summary in `docs/case-study.md`
- [ ] Push repo to GitHub with clean project structure
- [ ] (Optional) Deploy to Streamlit Cloud or HuggingFace Spaces

**Output:**
- `README.md`
- `docs/case-study.md`
- Public GitHub repository

---

## 📆 Timeline Summary

| Milestone                        | Est. Duration |
|----------------------------------|---------------|
| Milestone 1: Setup & Design      | 1 day         |
| Milestone 2: Core MVP            | 2–3 days      |
| Milestone 3: Logging             | 1 day         |
| Milestone 4: Dashboard           | 1–2 days      |
| Milestone 5: Packaging           | 1 day         |
| **Total Time**                   | **6–8 days**  |

---

## 🔄 Optional Stretch Goals

| Feature | Value |
|--------|-------|
| ✅ Teams/Slack integration | Real-world input source |
| ✅ Confidence scoring or fallback | More robust system |
| ✅ Human-in-the-loop verification | Improve trust |
| ✅ Admin panel for triage override | Real ops support |
| ✅ Multilingual prompt support | Localized workplace |

---

## 🚀 Goal

This plan will help build a clean, testable, and demo-friendly version of OfficeGenie for enterprise support automation.
