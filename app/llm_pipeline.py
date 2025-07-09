from dotenv import load_dotenv
from openai import OpenAI
from prompts import prompt_template

load_dotenv()  # Load environment variables from .env file

client = OpenAI()

llm_input = prompt_template.format(
    full_name="Ritika Das",
    email="ritika.das@company.com",
    department="Finance",
    message="Can you help me with my travel reimbursement for the client visit last week?"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": llm_input
        }
    ]
)

print(completion.choices[0].message.content)