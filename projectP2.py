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
        if param is None:
            print("Error Needs <param_street_name>.")
            sys.exit(1)
        query = """
        SELECT *
        FROM Site 
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
        if param is None:
            print("Error Needs <param_schedular_system>.")
            sys.exit(1)
        query = """
        SELECT d.serialNo, d.modelNo, t.name
        FROM DigitalDisplay d
        JOIN Specializes s ON d.modelNo = s.modelNo
        JOIN TechnicalSupport t ON s.empId = t.empId
        WHERE LOWER(d.schedulerSystem) = LOWER(%s);
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
    case "4":  
        if param is None:
            print("Error Needs <param_phone_no>.")
            sys.exit(1)
        query = """
        SELECT * 
        FROM Client
        WHERE phone = %s;
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
            print("EmpID\tName\t\tTotal Hours")
            for row in results:
                empId, name, total_hours = row
                print(f"{empId}\t{name}\t{total_hours}")
        else:
            print("No administrator work hours found.")
    case "6":
        if param is None:
            print("Error Needs <param_model_no>.")
            sys.exit(1)
        query = """
        SELECT T.name 
        FROM TechnicalSupport AS T 
        JOIN Specializes AS S ON T.empId = S.empId 
        WHERE S.modelNo = %s;
        """
        cursor.execute(query, (param,))
        results = cursor.fetchall()

        print("Technical Support Name(s):")
        for row in results:
            print(f"\t{row[0]}")
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

        print("Role\t\t\tcnt")
        print("------------------")
        for row in results:
            print(f"{row[0]}\t\t{row[1]}")
        
if connection.is_connected():
    cursor.close()
    connection.close()


