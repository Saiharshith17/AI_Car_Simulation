import mysql.connector
import json

# Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "1122",
    "database": "example"
}

file_path = "coordinates.json"

def load_coordinates_from_file(file_path):
    """Load coordinates and other parameters from a JSON file."""
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return (
                data["coordinates"], 
                data["speed"], 
                data["acceleration"], 
                data["max_speed"], 
                data["deceleration"], 
                data["turning_angle"]
            )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error loading JSON file:", e)
        return None, None, None, None, None, None

def get_model_weights(coordinates, speed, acceleration, max_speed, deceleration, turning_angle):
    """Retrieve the stored weights if all parameters match an entry in the database."""
    if not coordinates:
        print("No valid coordinates provided.")
        return

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Ensure JSON format in the query
        query = """
        SELECT weight_data FROM maps 
        WHERE JSON_CONTAINS(coordinates, CAST(%s AS JSON))
        AND speed = %s
        AND acceleration = %s
        AND max_speed = %s
        AND deceleration = %s
        AND turning_angle = %s
        LIMIT 1;
        """
        cursor.execute(query, (json.dumps(coordinates), speed, acceleration, max_speed, deceleration, turning_angle))
        result = cursor.fetchone()

        if result:
            weight_data = result[0]  # Retrieve weight_data from the database
            print("Weight Data:", weight_data)
            return weight_data
        else:
            print("No matching map found.")

    except mysql.connector.Error as err:
        print("Database error:", err)

    finally:
        cursor.close()
        conn.close()

# Load data from JSON file
if __name__ == "__main__":
    coordinates, speed, acceleration, max_speed, deceleration, turning_angle = load_coordinates_from_file(file_path)

    if coordinates is not None:
        weights = get_model_weights(coordinates, speed, acceleration, max_speed, deceleration, turning_angle)
        if weights:
            print("Retrieved Weights:", weights)
