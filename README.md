# 🧞 OfficeGenie – Smart Workplace Helpdesk

OfficeGenie is an AI-powered assistant that acts as a first-line triage system for employee support requests. It classifies natural language queries (e.g., IT, HR, Admin), extracts key details, and routes the issue to the correct team — with an instant response.

---

## ✨ Features

- 📝 Accepts user queries via web form
- 🧠 Classifies requests (IT, HR, Payroll, etc.)
- 🔍 Extracts structured info like system names, urgency, dates, etc.
- 📬 Sends automated acknowledgment
- 🔁 Routes request to the right department or automation
- 📊 Logs requests for future analytics

---

## 📦 Tech Stack

- **Frontend**: React
- **Backend**: Python 3.10+
- **LLM**: OpenAI GPT / Claude (via API)
- **Data**: JSON-based input/output + optional SQLite
- **Other**: Pandas, Prompt templating, Logging

---

## 🧪 Sample Use Case

> **User Message:** "I can't access my payslip for June. It shows 'file not found'. Please help."

**Predicted Output:**

```json
{
  "category": "Payroll",
  "subcategory": "Payslip Access",
  "extracted_fields": {
    "month": "June",
    "error_message": "file not found"
  },
  "suggested_response": "Hi Ananya, we've shared your payslip issue with the Payroll team. You’ll get an update shortly."
}
```

---

## 📁 Project Structure

```
officegenie/
├── docs/
│   ├── product/     # Product specs, ideas, and roadmaps
│   └── design/      # UI mockups, wireframes, and design assets
├── main.py          # Main application entry point
└── pyproject.toml   # Project dependencies and configuration
```

---

## 👤 Author

<table>
  <tr>
    <td>
      <img src="https://avatars.githubusercontent.com/your-github-username" width="100px" style="border-radius: 50%;" alt="Author Avatar"/>
    </td>
    <td>
      <b>Sumit Das</b>  
      <br/>
      🚀 Lead Research Engineer | Generative AI & NLP  
      <br/>
      🔗 <a href="https://www.linkedin.com/in/sumit-das-0132b825" target="_blank">LinkedIn</a> • 
      💻 <a href="https://github.com/sumitdas1984" target="_blank">GitHub</a> • 
      📫 <a href="mailto:sumit.jucse@gmail.com">Email</a>
    </td>
  </tr>
</table>

---

## 🏷️ Badges

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Built%20With-Streamlit-red?logo=streamlit)
![OpenAI](https://img.shields.io/badge/Powered%20By-OpenAI-azure?logo=openai&logoColor=white)
![MIT License](https://img.shields.io/badge/license-MIT-green)

