from db import get_db_connection
import psycopg2
from queries import *


def normalize_db():
    new_conn = get_db_connection()
    source_conn = psycopg2.connect(
        dbname="wwii_missions",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

    try:
        # execute the queries
        cur = new_conn.cursor()
        cur.execute(create_table_country)
        cur.execute(create_table_city)
        cur.execute(create_table_target_location)
        cur.execute(create_table_target)
        cur.execute(create_table_mission)
        # cur.executemany([create_table_country,
        #                  create_table_city,
        #                  create_table_target_location,
        #                  create_table_target,
        #                  create_table_mission])
        new_conn.commit()

        s_cur = source_conn.cursor()
        s_cur.execute("SELECT * FROM mission")
        while True:
            mission_row = s_cur.fetchone()
            if mission_row is None:
                break

            mission_date = mission_row[1]
            theater_of_operations = mission_row[2]
            country = mission_row[3]
            air_force = mission_row[4]
            unit_id = mission_row[5]
            aircraft_series = mission_row[6]
            callsign = mission_row[7]
            mission_type = mission_row[8]
            takeoff_base = mission_row[9]
            takeoff_location = mission_row[10]
            takeoff_latitude = mission_row[11]
            takeoff_longitude = mission_row[12]
            target_key = mission_row[13]
            target_country = mission_row[14]
            target_city = mission_row[15]
            target_type = mission_row[16]
            target_industry = mission_row[17]
            target_priority = mission_row[18]
            target_latitude = mission_row[19]
            target_longitude = mission_row[20]
            altitude_hundreds_of_feet = mission_row[21]
            airborne_aircraft = mission_row[22]
            attacking_aircraft = mission_row[23]
            bombing_aircraft = mission_row[24]
            aircraft_returned = mission_row[25]
            aircraft_failed = mission_row[26]
            aircraft_damaged = mission_row[27]
            aircraft_lost = mission_row[28]
            high_explosives = mission_row[29]
            high_explosives_type = mission_row[30]
            high_explosives_weight_pounds = mission_row[31]
            high_explosives_weight_tons = mission_row[32]
            incendiary_devices = mission_row[33]
            incendiary_devices_type = mission_row[34]
            incendiary_devices_weight_pounds = mission_row[35]
            incendiary_devices_weight_tons = mission_row[36]
            fragmentation_devices = mission_row[37]
            fragmentation_devices_type = mission_row[38]
            fragmentation_devices_weight_pounds = mission_row[39]
            fragmentation_devices_weight_tons = mission_row[40]
            total_weight_pounds = mission_row[41]
            total_weight_tons = mission_row[42]
            time_over_target = mission_row[43]
            bomb_damage_assessment = mission_row[44]
            source_id = mission_row[45]

            insert_country = """
            INSERT INTO country (country_name)
            VALUES (%s) RETURNING country_id;
            """
            params_country = (target_country,)

            cur.execute(insert_country, params_country)
            country_id = cur.fetchone()[0]

            insert_city = """
            INSERT INTO city (city_name, country_id)
            VALUES (%s, %s) RETURNING city_id;
            """
            params_city = (target_city, country_id,)

            cur.execute(insert_city, params_city)
            city_id = cur.fetchone()[0]

            insert_location = """
            INSERT INTO target_location (latitude, longitude, city_id)
            VALUES (%s, %s, %s) RETURNING target_location_id;
            """
            params_location = (target_latitude, target_longitude, city_id,)

            cur.execute(insert_location, params_location)
            target_location_id = cur.fetchone()[0]

            insert_target = """
            INSERT INTO target (target_type, target_industry, target_priority, target_location_id)
            VALUES (%s, %s, %s, %s) RETURNING target_id;
            """

            params_target = (target_type, target_industry, target_priority, target_location_id,)
            cur.execute(insert_target, params_target)
            target_id = cur.fetchone()[0]

            insert_mission = f"""
            INSERT INTO mission (mission_date, theater_of_operations, country, air_force, unit_id,
            aircraft_series, callsign, mission_type, takeoff_base, takeoff_location, takeoff_latitude,
            takeoff_longitude, target_key, target_id, altitude_hundreds_of_feet, airborne_aircraft,
            attacking_aircraft, bombing_aircraft, aircraft_returned, aircraft_failed, aircraft_damaged,
            aircraft_lost, high_explosives, high_explosives_type, high_explosives_weight_pounds,
            high_explosives_weight_tons, incendiary_devices, incendiary_devices_type,
            incendiary_devices_weight_pounds, incendiary_devices_weight_tons, fragmentation_devices,
            fragmentation_devices_type, fragmentation_devices_weight_pounds, fragmentation_devices_weight_tons,
            total_weight_pounds, total_weight_tons, time_over_target, bomb_damage_assessment, source_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """

            params_mission = (mission_date, theater_of_operations, country, air_force, unit_id,
            aircraft_series, callsign, mission_type, takeoff_base, takeoff_location, takeoff_latitude,
            takeoff_longitude, target_key, target_id, altitude_hundreds_of_feet, airborne_aircraft,
            attacking_aircraft, bombing_aircraft, aircraft_returned, aircraft_failed, aircraft_damaged,
            aircraft_lost, high_explosives, high_explosives_type, high_explosives_weight_pounds,
            high_explosives_weight_tons, incendiary_devices, incendiary_devices_type,
            incendiary_devices_weight_pounds, incendiary_devices_weight_tons, fragmentation_devices,
            fragmentation_devices_type, fragmentation_devices_weight_pounds, fragmentation_devices_weight_tons,
            total_weight_pounds, total_weight_tons, time_over_target, bomb_damage_assessment, source_id,)

            cur.execute(insert_mission,params_mission)
            new_conn.commit()



    except Exception as e:
        print(f"An error occurred: {e}")
        pass
    finally:
        pass


def get_len_mission():
    source_conn = psycopg2.connect(
        dbname="wwii_missions_normal",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
    cur = source_conn.cursor()
    cur.execute("SELECT * FROM mission")
    print(len(cur.fetchall()))

if __name__ == "__main__":
    normalize_db()
    get_len_mission()