from openai import OpenAI
import os
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

def load_prompt(filename):
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompts_dir = os.path.join(root_dir, "prompts")
    filepath = os.path.join(prompts_dir, filename)
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def rewrite_query(user_query: str) -> list[str]:
    try:
        response = client.responses.create(
            instructions=load_prompt("rewrite_query_prompt.txt"),
            model="gpt-4.1",
            input=user_query
        )
        return json.loads(response.output_text.strip())
    except Exception as e:
        print(f"키워드 리라이팅 실패")
        print(f"{e}")
        return user_query