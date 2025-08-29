import streamlit as st
from utils import hwp_to_html
from dotenv import load_dotenv
from utils import make_response
from pydantic import BaseModel
load_dotenv()

prompt = """
다음 HTML 문서에서 업무분장 정보를 추출해주세요.

HTML 내용:
{html}

위 HTML에서 테이블 구조를 분석하여 다음 정보를 추출해주세요:
1. 문서 제목과 날짜
2. 부서별 구성원 정보:
    - 직위 (부장, 차장, 직원 등)
    - 성명
    - 전화번호 (있는 경우)
    - 담당 업무 목록 (•로 구분된 각 업무를 리스트로)
    - 대행자 (있는 경우)

부서가 여러 개인 경우 각 부서별로 구분하여 추출해주세요.
"""
 
class Person(BaseModel):
    이름: str
    담당: str
    업무: list[str]
    전화번호: str   

class Doc(BaseModel):
    persons: list[Person]
    제목: str
    날짜: str

hwp_file = st.file_uploader(
    "변환할 hwp 파일을 업로드하세요", 
    type=["hwp"],
    accept_multiple_files=False,)

if hwp_file is not None:
    html = hwp_to_html(hwp_file=hwp_file) # 위치 인자
    user_content = prompt.format(html=html)

    ai_response = make_response(
        user_content = user_content,
        response_format = Doc
    )

    obj: Doc=ai_response.parsed
    st.text(obj.제목, obj.날짜)
    for person in obj.persons:
        person.이름
        person.담당
        person.업무
        person.전화번호
    
    st.text(user_content)
    st.text(f"AI : {ai_response.parsed}")