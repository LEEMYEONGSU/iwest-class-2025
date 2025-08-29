import sqlite3

with sqlite3.connect("power_plant.db") as conn:
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS generation_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plant_name TEXT NOT NULL,
            generation_mw REAL NOT NULL,
            recorded_at TIMESTAMP NOT NULL,
            efficiency REAL,
            status TEXT DEFAULT 'normal'
        )
    """
    )
    conn.commit()
    print("✅ 데이터베이스와 테이블이 생성되었습니다!")