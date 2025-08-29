import pandas as pd
import streamlit as st

excel_file = st.file_uploader(
    "엑셀 파일을 업로드하세요",
    type=["xlsx", "xls"],
    accept_multiple_files=False,
)

if excel_file is not None:
    df = pd.read_excel(excel_file)
    st.write(f"엑셀 파일 업로드 완료: {excel_file.name}")
    st.write(f"데이터프레임 shape: {df.shape}")
    st.dataframe(df)

