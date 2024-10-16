# Tomas Urena, Lin Wang, Mingfang Zhu
# 10/10/2024
# Project Part 2

import mysql.connector
import sys

if len(sys.argv) < 2:
    print("Error Needs Querery Number.")
    sys.exit(1)

try:
    connection = mysql.connector.connect(
    host = 'localhost',
    database = 'cs482502',
    user = 'dbuser',
    password = 'Iwilldowell')
    cursor = connection.cursor()
except mysql.connector.Error as err:
        print(f"Error: {err}")
        sys.exit(1)

questionNum = sys.argv[1]
param = sys.argv[2] if len(sys.argv) > 2 else None

match questionNum:
    case "1":
        query = """
        SELECT *
        FROM Sites 
        WHERE LOWER(address) LIKE %s;
        """
        cursor.execute(query, ('%' + param.lower() + '%',))
        results = cursor.fetchall()

        if results:
            print(f"Sites found on the street '{param}':")
            for row in results:
                print(f"id: {row[0]}, name: {row[1]}, Address: {row[2]}")
        else:
            print(f"No sites found on the street '{param}'.")
    case "2":
        query = """
        SELECT d.serial_no, d.model_no, t.name
        FROM DigitalDisplays d
        JOIN TechnicalSupports t ON d.model_no = t.model_no
        WHERE LOWER(d.scheduler_system) = LOWER(%s);
        """
        cursor.execute(query, (param,))
        results = cursor.fetchall()

        if results:
            print("Digital Displays with the given scheduler system:")
            for row in results:
                print(f"Serial No: {row[0]}, Model No: {row[1]}, Technical Support: {row[2]}")
        else:
            print(f"No digital displays found with scheduler system: {param}")
    case "3":
        query = """
        SELECT name, COUNT(*) AS cnt
        FROM Salesman
        GROUP BY name
        ORDER BY name ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        print("Name\tCount")
        
        for row in results:
            name, count = row
            print(f"{name}\t{count}")

            # If count > 1, show the full attributes
            if count > 1:
                query_details = """
                SELECT empId, name, gender
                FROM Salesman
                WHERE name = %s;
                """
                cursor.execute(query_details, (name,))
                details = cursor.fetchall()
                # print(f"Details for {name}:")
                # for detail in details:
                #     empId, name, gender = detail
                #     print(f"({empId}, {name}, {gender})")
                # print("-" * 30)
                
                detail_str = ', '.join([f"({empId}, {name}, {gender})" for empId, name, gender in details])
                print(f"{detail_str}")
    case "4":
        query = """
        SELECT * 
        FROM Client
        WHERE phone_no = %s;
        """
        cursor.execute(query, (param,))
        results = cursor.fetchall()
        
        if results:
            print(f"Clients with phone number '{param}':")
            for row in results:
                clientId, name, phone, address = row
                print(f"ID: {clientId}, Name: {name}, Phone: {phone}, Address: {address}")
        else:
            print(f"No clients found with phone number: {param}")
    case "5":
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
            print("EmpID\tName\tTotal Hours")
            for row in results:
                empId, name, total_hours = row
                print(f"{empId}\t{name}\t{total_hours}")
        else:
            print("No administrator work hours found.")
    case "6":
        query = """
        SELECT T.name 
        FROM TechnicalSupport AS T 
        JOIN Specializes AS S ON T.empId = S.empId 
        WHERE S.modelNo = %s;
        """
        cursor.execute(query, (param,))
        results = cursor.fetchall()

        for row in results:
            print(row[0])
    case "7": 
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
    case "8":
        query = """
        SELECT 'Administrator' AS Role, COUNT(*) AS C FROM Administrator 
        UNION 
        SELECT 'Salesman' AS Role, COUNT(*) AS C FROM Salesman 
        UNION 
        SELECT 'Technician' AS Role, COUNT(*) AS C FROM TechnicalSupport;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            print(f"Role\t\tcnt \n{row[0]}\t\t{row[1]}")
        
if connection.is_connected():
    cursor.close()
    connection.close()


