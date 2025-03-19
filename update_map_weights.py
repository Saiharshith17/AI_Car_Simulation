import mysql.connector
import json

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1122",
    "database": "example"
}

def load_coordinates_from_file(file_path):
    """Load coordinates from a JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data["coordinates"]
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error loading JSON file:", e)
        return None

def get_weight_data(coordinates):
    """Retrieve weight data if the given coordinates match any map."""
    if not coordinates:
        print("No valid coordinates provided.")
        return None

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Query to check if coordinates exist
        query = "SELECT weight_data FROM maps WHERE JSON_CONTAINS(coordinates, %s) LIMIT 1;"
        cursor.execute(query, (json.dumps(coordinates),))
        result = cursor.fetchone()

        if result:
            weight_data = json.loads(result[0])  # Parse JSON weight data
            print("Weight data found:", weight_data)
            return weight_data
        else:
            print("No matching map found.")
            return None

    except mysql.connector.Error as err:
        print("Database error:", err)
        return None

    finally:
        cursor.close()
        conn.close()

# Load coordinates from JSON file
file_path = "coordinates.json"  # Ensure this file exists in the project directory
coordinates = load_coordinates_from_file("coordinates.json")

# Call function to get weight data
if coordinates:
    weight_data = get_weight_data(coordinates)
