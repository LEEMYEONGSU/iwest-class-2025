import os
from dotenv import load_dotenv
from openai import OpenAI
from tasks import create_email_body, summarize_meeting

load_dotenv()  # 프로그램의 진입점에서 한번만 실행
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default=None) or None

# email_body = create_email_body(
#     받는사람 = "이진석 대리",   #keyword parameter
#     용건 = "8월 업무보고",
#     핵심내용 = "우리 휴가 언제가나.",
#     api_key=OPENAI_API_KEY
# )

# print(create_email_body)

with open("./회의록/20250825.txt", "rt", encoding="utf-8") as file:
    회의록 = file.read()    #파일의 전체 내용을 읽어서, 문자열로 반환

요약내용 = summarize_meeting(회의록=회의록, api_key=OPENAI_API_KEY)
print("## 요약 내용 ##")
print(요약내용)