import mysql.connector
import json

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1122",
    "database": "example"
}

file_path = "coordinates1.json"

def load_data_from_file(file_path):
    """Load all data from the JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return (
                data["map_name"],
                data["coordinates"], 
                data["speed"], 
                data["acceleration"], 
                data["max_speed"], 
                data["deceleration"], 
                data["turning_angle"],
                data["weight_data"]
            )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error loading JSON file:", e)
        return None, None, None, None, None, None, None, None

def insert_map_data(map_name, coordinates, speed, acceleration, max_speed, deceleration, turning_angle, weight_data):
    """Insert data into MySQL, avoiding duplicates."""
    if not coordinates:
        print("No valid coordinates provided.")
        return

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if entry already exists
        check_query = """
        SELECT COUNT(*) FROM maps WHERE 
        map_name = %s AND
        JSON_CONTAINS(coordinates, CAST(%s AS JSON)) AND 
        ROUND(speed, 2) = ROUND(%s, 2) AND 
        ROUND(acceleration, 2) = ROUND(%s, 2) AND 
        ROUND(max_speed, 2) = ROUND(%s, 2) AND 
        ROUND(deceleration, 2) = ROUND(%s, 2) AND 
        ROUND(turning_angle, 2) = ROUND(%s, 2);
        """
        cursor.execute(check_query, (map_name, json.dumps(coordinates), speed, acceleration, max_speed, deceleration, turning_angle))
        exists = cursor.fetchone()[0]

        if exists:
            print("Entry already exists in the database.")
            return

        # Insert data into the database
        query = """
        INSERT INTO maps (map_name, coordinates, speed, acceleration, max_speed, deceleration, turning_angle, weight_data) 
        VALUES (%s, CAST(%s AS JSON), %s, %s, %s, %s, %s, CAST(%s AS JSON));
        """
        cursor.execute(query, (map_name, json.dumps(coordinates), speed, acceleration, max_speed, deceleration, turning_angle, json.dumps(weight_data)))
        conn.commit()

        print("Data inserted successfully!")

    except mysql.connector.Error as err:
        print("Database error:", err)

    finally:
        cursor.close()
        conn.close()

# Load data from JSON file and insert into the database
if __name__ == "__main__":
    map_name, coordinates, speed, acceleration, max_speed, deceleration, turning_angle, weight_data = load_data_from_file(file_path)

    if coordinates is not None:
        insert_map_data(map_name, coordinates, speed, acceleration, max_speed, deceleration, turning_angle, weight_data)
