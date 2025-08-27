import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default=None) or None
print(repr(OPENAI_API_KEY))

client = OpenAI(api_key=OPENAI_API_KEY) 
messages = [
        {   "role" : "system", "content": "당신은 서부발전의 장장장 대리입니다"}
    ]

# user_content = input("Human : ").strip()
# messages.append(
#      {   "role" : "user", "content": user_content}
# )
while True:
    user_content = input("Human : ").strip()
    if user_content in ["", "quit"]:
        break

    messages.append(
        {"role" : "user", "content": user_content}
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )

    assistant_content: str = response.choices[0].message.content
    messages.append(
        {"role": "assistant", "content": assistant_content}
    )
    print("AI : ", assistant_content)

    # print("response.usage : ", response.usage)
    # print(response.choices[0].message.content)
