import mysql.connector
import sys

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
        FROM Site 
        WHERE LOWER(address) LIKE %s;
        """
        cursor.execute(query, ('%' + street_name.lower() + '%',))
        results = cursor.fetchall()

        if results:
            print(f"Sites found on the street '{street_name}':")
            for row in results:
                print(f"id: {row[0]}, name: {row[1]}, Address: {row[2]}, Phone: {row[3]}")
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
        SELECT d.serialNo, d.modelNo, t.name
        FROM DigitalDisplay d
        JOIN Specializes s ON d.modelNo = s.modelNo
        JOIN TechnicalSupport t ON s.empId = t.empId
        WHERE LOWER(d.schedulerSystem) = LOWER(%s);
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


# Function to list salesmen and count occurrences
def list_salesmen():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT name, COUNT(*) AS cnt
        FROM Salesman
        GROUP BY name
        ORDER BY name ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Name\t\tCount")
        print("------------------")
        for row in results:
            name, count = row
            detail_str = ''
            # If count > 1, show the full attributes
            if count > 1:
                query_details = """
                SELECT empId, name, gender
                FROM Salesman
                WHERE name = %s;
                """
                cursor.execute(query_details, (name,))
                details = cursor.fetchall()
                detail_str = ', '.join([f"({empId}, {name}, {gender})" for empId, name, gender in details])
            print(f"{name}\t{count} {detail_str}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to find clients with a given phone number
def find_clients(phone_no):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT * 
        FROM Client
        WHERE phone = %s;
        """
        cursor.execute(query, (phone_no,))
        results = cursor.fetchall()

        if results:
            print(f"Clients with phone number '{phone_no}':")
            for row in results:
                clientId, name, phone, address = row
                print(f"ID: {clientId}, Name: {name}, Phone: {phone}, Address: {address}")
        else:
            print(f"No clients found with phone number: {phone_no}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to find total working hours of each administrator
def total_working_hours():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT a.empId, a.name, SUM(w.hours) AS total_hours
        FROM Administrator a
        JOIN AdmWorkHours w ON a.empId = w.empId
        GROUP BY a.empId, a.name
        ORDER BY total_hours ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            print("EmpID\tName\t\tTotal Hours")
            for row in results:
                empId, name, total_hours = row
                print(f"{empId}\t{name}\t{total_hours}")
        else:
            print("No administrator work hours found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to find technical supports specializing in a given model
def find_technical_supports(model_no):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT T.name 
        FROM TechnicalSupport AS T 
        JOIN Specializes AS S ON T.empId = S.empId 
        WHERE S.modelNo = %s;
        """
        cursor.execute(query, (model_no,))
        results = cursor.fetchall()

        print("Technical Support Name(s):")
        for row in results:
            print(f"\t{row[0]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to order salesmen by average commission rate
def order_salesmen_by_commission():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT S.name, AVG(P.commissionRate) AS avgCommissionRate 
        FROM Salesman AS S 
        JOIN Purchases AS P ON S.empId = P.empId 
        GROUP BY S.name 
        ORDER BY avgCommissionRate DESC;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            print(f"Name: {row[0]}, Avg Commission Rate: {row[1]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Function to count roles in the company
def count_roles():
    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        query = """
        SELECT 'Administrator' AS Role, COUNT(*) AS C FROM Administrator 
        UNION 
        SELECT 'Salesman' AS Role, COUNT(*) AS C FROM Salesman 
        UNION 
        SELECT 'Technician' AS Role, COUNT(*) AS C FROM TechnicalSupport;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        print("Role\t\t\tcnt")
        print("------------------")
        for row in results:
            print(f"{row[0]}\t\t{row[1]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# Main function to execute based on query number
def main():
    if len(sys.argv) < 2:
        print("Error Needs Query Number.")
        sys.exit(1)

    query_number = sys.argv[1]
    param = sys.argv[2] if len(sys.argv) > 2 else None

    match query_number:
        case "1":
            if param is None:
                print("Error Needs <param_street_name>.")
                sys.exit(1)
            find_sites_on_street(param)
        case "2":
            if param is None:
                print("Error Needs <param_schedular_system>.")
                sys.exit(1)
            find_digital_displays_with_scheduler(param)
        case "3":
            list_salesmen()
        case "4":
            if param is None:
                print("Error Needs <param_phone_no>.")
                sys.exit(1)
            find_clients(param)
        case "5":
            total_working_hours()
        case "6":
            if param is None:
                print("Error Needs <param_model_no>.")
                sys.exit(1)
            find_technical_supports(param)
        case "7":
            order_salesmen_by_commission()
        case "8":
            count_roles()
        case _:
            print("Invalid question number.")


# Entry point of the script
if __name__ == "__main__":
    main()

