import sqlite3
from dataclasses import dataclass

@dataclass      #장식자(Decorator)
class PowerPlant:
    id: int
    name: str

def get_power_plant_list(plant_name: str) -> list[PowerPlant]:
    power_plant_list = []

    with sqlite3.connect("power_plant.db") as conn:
        conn.row_factory = sqlite3.Row  # 조회되는 값이 dict 타입이 됩니다.
        cursor = conn.cursor()

        # id 내림차순, 처음 10개를 조회
        # sql = "select * from generation_data order by id desc limit 10"
        sql = "select id, plant_name from generation_data where plant_name = ?"
        params = [plant_name]
        cursor.execute(sql, params)
        for row in cursor:
            power_plant_list.append(
                    PowerPlant(
                        id = row["id"],
                        name = row["plant_name"]
                    )
            )
    return power_plant_list

print(get_power_plant_list("태안발전소"))