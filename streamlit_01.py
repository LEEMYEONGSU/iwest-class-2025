import streamlit as st
from dotenv import load_dotenv
from utils import make_response

load_dotenv()

st.title("한국서부발전")

st.markdown(
    """
    안녕하세요
    """
)

question = st.text_input("질문을 입력하세요.")
if st.button("전송") and question:
   ai_content = make_response(user_content=question)
   st.write(f"AI: {ai_content}")