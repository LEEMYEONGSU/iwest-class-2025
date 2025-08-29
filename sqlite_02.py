import sqlite3
from datetime import datetime


# datetime 타입에 대한 변환 어댑터 지정
def adapt_datetime_to_iso(dt: datetime) -> str:
    return dt.isoformat()

sqlite3.register_adapter(datetime, adapt_datetime_to_iso)


with sqlite3.connect("power_plant.db") as conn:
    cursor = conn.cursor()

    # 단일 데이터 입력
    cursor.execute('''
        INSERT INTO generation_data (plant_name, generation_mw, recorded_at, efficiency)
        VALUES (?, ?, ?, ?)
    ''', ('태안발전소', 3400.5, datetime.now(), 42.5))

    # 여러 데이터 한번에 입력 (데이터 건수가 많을 경우, 유리)
    data_batch = [
        ('태안발전소', 3450.2, datetime.now(), 43.1),
        ('평택발전소', 2800.7, datetime.now(), 41.8),
        ('서인천발전소', 1950.3, datetime.now(), 44.2),
    ]
    cursor.executemany('''
        INSERT INTO generation_data (plant_name, generation_mw, recorded_at, efficiency)
        VALUES (?, ?, ?, ?)
    ''', data_batch)

    conn.commit()
    print(f"✅ {cursor.rowcount}개의 데이터가 저장되었습니다!")