import streamlit as st
from utils import make_response
from dotenv import load_dotenv

load_dotenv()

user_content = st.text_input("지시사항 :") or "이 이미지를 보고 설명해줘"

image_file = st.file_uploader(
    "이미지를 업로드하세요",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=False,
)

if image_file is not None:
    st.write(f"업로드 완료: {image_file}")
    ai_content = make_response(
        user_content = user_content,
        image_file =image_file,
    )
    st.write(f"AI: {ai_content}")