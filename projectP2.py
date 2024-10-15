# Tomas Urena, Lin Wang, Mingfang Zhu
# 10/10/2024
# Project Part 2

import mysql.connector
import sys

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
if(sys.argv[2] is None):
    param = sys.argv[2]

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
        print()
    case "4":
        print()
    case "5":
        print()
    case "6":
        query = "SELECT T.name FROM TechnicalSupport AS T JOIN Specializes AS S ON T.empId = S.empId WHERE S.modelNo = " + param + ";"
        results = cursor.execute_query(query)
        for row in results:
            print(row)
    case "7": 
        query = "SELECT S.name, AVG(P.commissionRate) AS avgCommissionRate FROM Salesman AS S JOIN Purchases AS P ON S.empId = P.empId GROUP BY S.name ORDER BY avgCommissionRate DESC;"
        results = cursor.execute_query(query)
        for row in results:
            print(row)
    case "8":
        query = "SELECT 'Administrator' AS Role, COUNT(*) AS C FROM Administrator UNION SELECT 'Salesman' AS Role, COUNT(*) AS C FROM Salesman UNION SELECT 'Technician' AS Role, COUNT(*) AS C FROM TechnicalSupport;"
        results = cursor.execute_query(query)
        for row in results:
            print(row)
        
if connection.is_connected():
    cursor.close()
    connection.close()


