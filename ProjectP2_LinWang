
import sys
import mysql.connector

# Function to connect to the database
def connect_to_db():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='cs482502',
            user='dbuser',
            password='Iwilldowell'
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)


# Function to find sites on a given street
def find_sites_on_street(street_name):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT *
        FROM Sites 
        WHERE LOWER(address) LIKE %s;
        """
        cursor.execute(query, ('%' + street_name.lower() + '%',))
        results = cursor.fetchall()

        if results:
            print(f"Sites found on the street '{street_name}':")
            for row in results:
                print(f"id: {row[0]}, name: {row[1]}, Address: {row[2]}")
        else:
            print(f"No sites found on the street '{street_name}'.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to find digital displays with a given scheduler system
def find_digital_displays_with_scheduler(scheduler_system):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT d.serial_no, d.model_no, t.name
        FROM DigitalDisplays d
        JOIN TechnicalSupports t ON d.model_no = t.model_no
        WHERE LOWER(d.scheduler_system) = LOWER(%s);
        """
        cursor.execute(query, (scheduler_system,))
        results = cursor.fetchall()

        if results:
            print("Digital Displays with the given scheduler system:")
            for row in results:
                print(f"Serial No: {row[0]}, Model No: {row[1]}, Technical Support: {row[2]}")
        else:
            print(f"No digital displays found with scheduler system: {scheduler_system}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def main():
    if len(sys.argv) < 3:
        print("Usage: python proj.py <query_number> <param>")
        sys.exit(1)

    query_number = sys.argv[1]
    param = sys.argv[2]

    if query_number == "1":
        find_sites_on_street(param)
    elif query_number == "2":
        find_digital_displays_with_scheduler(param)
    else:
        print("Invalid command.")


# Entry point of the script
if __name__ == "__main__":
    main()

