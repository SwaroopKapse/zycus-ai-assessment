# Zycus AI Assessment

An AI-powered customer support and account intelligence system built using Python, retrieval-based knowledge search, LLM-powered analysis, and evaluation pipelines.

## Project Overview

The project contains three major tasks:

### Task 1 — AI Support Ticket Triage

The system analyzes customer support tickets and determines:

- Product area
- Issue category
- Urgency
- Reasoning
- Whether the issue is a known issue
- Relevant knowledge-base documents
- Recommended support team
- Draft customer response

The system retrieves relevant knowledge-base documents before sending the ticket context to the LLM.
the app folder is contain  task 1 

### Task 2 — Account Health Brief

The system generates an account health brief using:

- Account information
- Usage trends
- ARR
- Open tickets
- Escalation notes
- Recent ticket history
- Customer information

The system analyzes only the supplied account and ticket data and avoids inventing unsupported information.

### Task 3 — Evaluation

Task 3 evaluates the outputs of Task 1 and Task 2 against predefined test cases.

Current evaluation result:

- Task 1: 100%
- Task 2: 100%
- Overall: 100%

###### LOOM WALKTHROUGH : https://www.loom.com/share/fb48af4d7f48445693b0cec78aa34c4f

## Project Structure

```text
zycus-ai-assessment/
│
├── app/
│   ├── api.py
│   ├── data_loader.py
│   ├── kb_loader.py
│   ├── llm_client.py
│   ├── prompts.py
│   ├── retriever.py
│   ├── routing.py
│   ├── schemas.py
│   └── triage.py
│
├── task2/
│   ├── account_health.py
│   └── test_account_health.py
│
├── task3/
│   ├── eval_task1.py
│   ├── eval_task2.py
│   ├── run_evaluation.py
│   └── eval_report.json
│
├── data/
│   ├── accounts.json
│   └── tickets.json
│
├── knowlege-base/
│
├── requirements.txt
├── .env.example
└── README.md


Setup
Create a virtual environment:

python3 -m venv .venv

Activate it:
source .venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Configure the required API key in .env.
Example:
GROQ_API_KEY=your_api_key_here

Running Task 1
python app/test_triage.py

For multiple tickets:
python app/test_multiple_triage.py

Running Task 2
python -m task2.test_account_health

Running Task 3
python -m task3.run_evaluation

The evaluation report is generated at:
task3/eval_report.json

Evaluation Result
The current evaluation passes all provided Task 1 and Task 2 test cases.
Task 1 Score : 1.00
Task 2 Score : 1.00
Overall Score: 1.00

Technologies
Python
FastAPI
Pydantic
Groq LLM API
Retrieval-based knowledge search
JSON data processing
Knowledge-base document retrieval


