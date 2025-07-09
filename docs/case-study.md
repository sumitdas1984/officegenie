# 📖 Case Study: OfficeGenie

## 🎯 Problem

Employees send helpdesk queries in unstructured form (chat, email), causing delays in routing and resolution.

## 🧠 Solution

Build an LLM-powered language triage agent that:

- Understands natural language requests
- Extracts structured info
- Routes requests intelligently
- Sends automated responses

## 🧪 Dataset

20+ synthetic queries covering:
- IT (VPN, laptop, access)
- HR (leave balance, update info)
- Finance (salary, tax forms)
- Admin (AC, bookings)

## 🧠 LLM Prompts

Used OpenAI GPT-4 via LangChain with few-shot prompt engineering.

## 📊 Evaluation

- ~90% accuracy on category prediction (synthetic set)
- Real-time processing < 2s per query

## 📍 Learnings

- Prompt robustness matters more than model
- Adding department/user context boosts accuracy
- Auto-response personalization builds trust

