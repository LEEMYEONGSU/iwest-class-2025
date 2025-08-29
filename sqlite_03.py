import sqlite3

with sqlite3.connect("power_plant.db") as conn:
    cursor = conn.cursor()
    conn.row_factory = sqlite3.Row  # 조회되는 값이 dict 타입이 됩니다.

    # id 내림차순, 처음 10개를 조회
    # sql = "select * from generation_data order by id desc limit 10"
    sql = "select id, plant_name from generation_data where plant_name = ?"
    params = ["태안발전소"]
    cursor.execute(sql, params)
    rows: list = cursor.fetchall()

    # for row in rows: # rol => tuple
    #     print(row[0]) # id
    #     print(row[1]) # plant_name

    for row in rows:
        print(row) # 아마도 dict 타입
    conn.commit()
