from db import *


def create_indexes():
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        index_queries = [
            "CREATE INDEX IF NOT EXISTS idx_mission_date ON mission(mission_date);",
            "CREATE INDEX IF NOT EXISTS idx_air_force ON mission(air_force);",
            "CREATE INDEX IF NOT EXISTS idx_target_city ON mission(target_city);",
            "CREATE INDEX IF NOT EXISTS idx_airborne_aircraft ON mission(\"airborne_aircraft\");",
            "CREATE INDEX IF NOT EXISTS idx_bomb_damage_assessment ON mission(\"bomb_damage_assessment\");",
            "CREATE INDEX IF NOT EXISTS idx_target_country ON mission(\"target_country\");",
            "CREATE INDEX IF NOT EXISTS idx_air_force_target_city ON mission(air_force, target_city);",
            "CREATE INDEX IF NOT EXISTS idx_airborne_bomb_damage ON mission(\"airborne_aircraft\", \"bomb_damage_assessment\");"
        ]

        for query in index_queries:
            cursor.execute(query)
        conn.commit()

    finally:
        pass


def get_air_force_missions_by_city(year):
    query = """
        SELECT 
            m.air_force,
            COUNT(m.mission_id) AS number_of_missions
        FROM 
            mission m
        WHERE 
            EXTRACT(YEAR FROM m.mission_date) = %s
            AND m.air_force IS NOT NULL
        GROUP BY 
            m.air_force
        ORDER BY 
            number_of_missions DESC
        LIMIT 1;
        """

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(query, (year,))

        result = cur.fetchone()

        if result:
            air_force, number_of_missions = result
            most_active_air_force = {
                'air_force': air_force,
                'number_of_missions': number_of_missions
            }
        else:
            most_active_air_force = {
                'air_force': None,
                'number_of_missions': 0
            }

        cur.close()
        conn.close()

        return most_active_air_force

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_average_damage_by_country():
    query = """
        SELECT 
            country,
            AVG(CAST(bomb_damage_assessment AS NUMERIC)) AS average_damage
        FROM 
            mission
        WHERE 
            airborne_aircraft > 5
        GROUP BY 
            country;
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query)
        results = cursor.fetchall()

        average_damage_by_country = [
            {'country': row[0], 'average_damage': row[1]}
            for row in results
        ]

        cursor.close()
        conn.close()

        return average_damage_by_country

    except Exception as e:
        print(f"An error occurred: {e}")
        return None



if __name__ == "__main__":
    print(get_air_force_missions_by_city(1942))