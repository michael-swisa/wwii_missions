from db import get_db_connection


def get_mission_by_id(mission_id):
    coon = get_db_connection()
    cursor = coon.cursor()

    query = """
        SELECT 
            m.mission_type,
            m.takeoff_location,
            m.time_over_target,
            m.bomb_damage_assessment,
            m.country,
            m.mission_date,
            t.target_industry,
            t.target_priority,
            t.target_type,
            c.country_name AS target_country,
            ci.city_name AS target_city
        FROM 
            mission m
        LEFT JOIN 
            target t ON m.target_id = t.target_id
        LEFT JOIN 
            target_location tl ON t.target_location_id = tl.target_location_id
        LEFT JOIN 
            city ci ON tl.city_id = ci.city_id
        LEFT JOIN 
            country c ON ci.country_id = c.country_id
        WHERE 
            m.mission_id = %s;
    """

    cursor.execute(query, (mission_id,))
    result = cursor.fetchone()

    if result:
        mission_data = {
            'mission_type': result[0],
            'takeoff_location': result[1],
            'time_over_target': result[2],
            'bomb_damage_assessment': result[3],
            'country': result[4],
            'mission_date': result[5],
            'target_name': result[6],
            'target_type': result[7],
            'target_country': result[8],
            'target_city': result[9],
            'mission_name': result[10]
        }
        return mission_data
    else:
        return None

def get_all_missions_in_db():
    coon = get_db_connection()
    cursor = coon.cursor()

    query = """
        SELECT 
            m.mission_id,
            m.mission_type,
            m.takeoff_location,
            m.time_over_target,
            m.bomb_damage_assessment,
            m.country,
            m.mission_date,
            t.target_industry,
            t.target_priority,
            t.target_type,
            c.country_name AS target_country,
            ci.city_name AS target_city
        FROM 
            mission m
        LEFT JOIN 
            target t ON m.target_id = t.target_id
        LEFT JOIN 
            target_location tl ON t.target_location_id = tl.target_location_id
        LEFT JOIN 
            city ci ON tl.city_id = ci.city_id
        LEFT JOIN 
            country c ON ci.country_id = c.country_id
        LIMIT 1000
    """

    cursor.execute(query)
    results = cursor.fetchall()

    missions = []
    for result in results:
        mission_data = {
            'mission_id': result[0],
            'mission_type': result[1],
            'takeoff_location': result[2],
            'time_over_target': result[3],
            'bomb_damage_assessment': result[4],
            'country': result[5],
            'mission_date': result[6],
            'target_industry': result[7],
            'target_priority': result[8],
            'target_type': result[9],
            'target_country': result[10],
            'target_city': result[11]
        }
        missions.append(mission_data)

    return missions