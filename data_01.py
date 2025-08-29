import pandas as pd

excel_path = "./assets/list.xlsx"

# Data Frame 타입
# 엑셀 중에 첫번째 시트에 대해서만 반환

df = pd.read_excel(excel_path) # , sheet_name="")
print(df.shape) # (행, 열) 튜플
print(df.head())  # 앞에서부터 5개 행 출력

