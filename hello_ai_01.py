import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default=None) or None
print(repr(OPENAI_API_KEY))

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o",
    messages = [
        {   "role" : "system", "content": "당신은 서부발전의 장장장 대리입니다"},
        {   "role" : "user", "content": "자기소개를 해주세요. 이름 3행시도 지어주세요"}
    ]
)

print("response.usage : ", response.usage)
print(response.choices[0].message.content)

