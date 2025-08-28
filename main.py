import os
from dotenv import load_dotenv
from openai import OpenAI
from tasks import create_email_body

load_dotenv()  # 프로그램의 진입점에서 한번만 실행
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", default=None) or None

email_body = create_email_body(
    받는사람 = "이진석 대리",   #keyword parameter
    용건 = "8월 업무보고",
    핵심내용 = "우리 휴가 언제가나.",
    api_key=OPENAI_API_KEY
)

print(create_email_body)