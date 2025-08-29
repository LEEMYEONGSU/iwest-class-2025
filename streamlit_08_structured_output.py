from dotenv import load_dotenv
import streamlit as st
from utils import make_response
from pydantic import BaseModel

class Person(BaseModel):
    담당: str
    업무: list[str]

class PersonList(BaseModel):
    persons: list[Person]

load_dotenv()

input_textarea = st.text_area("추출할 텍스트를 입력하세요")

if input_textarea:
    user_content = "내용에서 각각의 담당, 업무를 JSON 포맷으로 출력해주세요 \n\n" + input_textarea
    ai_response = make_response(
        user_content = user_content,
        response_format = PersonList
    )
    obj: PersonList=ai_response.parsed
    for person in obj.persons:
        person.담당
        person.업무
    
    st.text(f"AI : {ai_response.parsed}")
    