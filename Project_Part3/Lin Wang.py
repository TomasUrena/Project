import mysql.connector
from mysql.connector import Error


def main():
    host = input("Enter database host: ")
    database = input("Enter database name: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=username,
            password=password
        )

        if connection.is_connected():
            print("\nSuccessfully connected to the database.")

            while True:
                # Displaying main options to the user
                print("\nMain Menu:")
                print("1. Display all the digital displays")
                print("2. Search digital displays given a scheduler system")
                print("3. Insert a new digital display")
                print('4. Delete a digital display')
                print('5. Update a digital display')
                print("6. Logout")

                choice = input("\nEnter your choice: ")

                if choice == '1':
                    display_digital_displays(connection)
                elif choice == '2':
                    search_digital_displays_by_schdulerSys(connection)
                elif choice == '3':
                    insert_new_digital_display(connection)
                elif choice == '4':
                    delete_digital_display(connection)
                elif choice == '5':
                    update_digital_display(connection)
                elif choice == '6':
                    print("Logging out...")
                    break
                else:
                    print("Invalid choice. Please try again.")

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")


def display_digital_displays(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT serialNo, modelNo FROM DigitalDisplay")
        displays = cursor.fetchall()

        if displays:
            print("\nDigital Displays:")
            for i, display in enumerate(displays, start=1):
                print(f"{i}. Serial No: {display[0]}, Model No: {display[1]}")

            model_choice = input(
                "\nEnter the number corresponding to the display to view detailed model information, or 'b' to go back: ")

            if model_choice.lower() == 'b':
                return

            if model_choice.isdigit() and 1 <= int(model_choice) <= len(displays):
                model_no = displays[int(model_choice) - 1][1]
                display_model_details(connection, model_no)
            else:
                print("Invalid choice. Returning to main menu.")
        else:
            print("No digital displays found.")

    except Error as e:
        print(f"Error: {e}")


def display_model_details(connection, model_no):
    try:
        cursor = connection.cursor()
        # Fetching model details from the database
        cursor.execute("SELECT * FROM Model WHERE modelNo = %s", (model_no,))
        model_details = cursor.fetchone()

        if model_details:
            print("\nModel Details:")
            print(f"Model No: {model_details[0]}")
            print(f"Width: {model_details[1]}")
            print(f"Height: {model_details[2]}")
            print(f"Weight: {model_details[3]}")
            print(f"Depth: {model_details[4]}")
            print(f"Screen Size: {model_details[5]}")
        else:
            print("Model details not found.")

    except Error as e:
        print(f"Error: {e}")
        
def search_digital_displays_by_schdulerSys(connection):
    try:
        schedulerSys = input("Enter scheduler system to search for: ")
        
        cursor = connection.cursor()
        cursor.execute("SELECT serialNo, modelNo FROM DigitalDisplay WHERE schedulerSystem = %s", (schedulerSys,))
        results = cursor.fetchall()
        
        if results:
            print("\nDigital Displays with Scheduler System '{}':".format(schedulerSys))
            for i, result in enumerate(results, start = 1):
                print(f"{i}. Serial No: {result[0]}, Model No: {result[1]}")
        else:
            print("Display not found.")
            
    except Error as e:
        print(f"Error: {e}")
        
def insert_new_digital_display(connection):
    try:
        serialNo = input("Enter serial number for the new digital display: ")
        scheduler_sys = input("Enter scheduler system for the new digital display: ")
        modelNo = input("Enter model number for the new digital display: ")
        
        cursor = connection.cursor()

        # Check if the digital display with the given serial number already exists
        cursor.execute("SELECT serialNo FROM DigitalDisplay WHERE serialNo = %s", (serialNo,))
        display_exists = cursor.fetchone()
        
        if display_exists:
            print("Digital display with this serial number already exists.")
            return  # Stop insertion if the serialNo already exists
        
        # Check if the model number exists in the Model table
        cursor.execute("SELECT modelNo FROM Model WHERE modelNo = %s", (modelNo,))
        model_exists = cursor.fetchone()
        
        # If the model does not exist, prompt user to add model details
        if not model_exists:
            print("Model does not exist. Please provide model details.")
            width = float(input("Enter model width: "))
            height = float(input("Enter model height: "))
            weight = float(input("Enter model weight: "))
            depth = float(input("Enter model depth: "))
            screen_size = float(input("Enter model screen size: "))

            # Insert the new model into the Model table
            cursor.execute(
                "INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES (%s, %s, %s, %s, %s, %s)",
                (modelNo, width, height, weight, depth, screen_size)
            )
            connection.commit()
            print("New model added to the Model table.")

        # Insert the new digital display into the DigitalDisplay table
        cursor.execute(
            "INSERT INTO DigitalDisplay (serialNo, schedulerSystem, modelNo) VALUES (%s, %s, %s)",
            (serialNo, scheduler_sys, modelNo)
        )
        connection.commit()
        print("New digital display added to the DigitalDisplay table.")

    except Error as e:
        print(f"Error: {e}")


def delete_digital_display(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DigitalDisplay")
        displays = cursor.fetchall()

        if displays:
            print("\nDigital Displays:")
            for i, display in enumerate(displays, start = 1):
                print(f"{i}. SerialNo: {display[0]}, SchedulerSystem: {display[1]}, ModelNo: {display[2]}")

            delete = input("\nEnter The Number Corresponding To The Display To Delete It, or 'b' to go back: ")

            if delete.lower() == 'b':
                return
            
            if delete.isdigit() and 1 <= int(delete) <= len(displays):
                serialNo = displays[int(delete) - 1][0]
                cursor.execute('''SELECT modelNo 
                            FROM DigitalDisplay 
                            WHERE serialNo = %s''', (serialNo,))
                modelNo = cursor.fetchone()
                if modelNo:
                    cursor.execute("DELETE FROM DigitalDisplay WHERE serialNo = %s", (serialNo,)) 
                    connection.commit()
                    cursor.execute("SELECT COUNT(*) FROM DigitalDisplay WHERE modelNo = %s", modelNo)
                    count = cursor.fetchone()[0]
                    if count == 0:
                        cursor.execute("DELETE FROM Model WHERE modelNo = %s", (modelNo))
                        connection.commit()
                    print('\nDisplay With SerialNo:', serialNo, 'deleted.')

                    cursor.execute("SELECT * FROM DigitalDisplay")
                    displays = cursor.fetchall()
                    print("\nDigital Displays:")
                    for i, display in enumerate(displays, start = 1):
                        print(f"{i}. SerialNo: {display[0]}, SchedulerSystem: {display[1]}, ModelNo: {display[2]}")

                    cursor.execute("SELECT * FROM Model")
                    models = cursor.fetchall()
                    print("\nModels:")
                    for i, model in enumerate(models, start = 1):
                        print(f"{i}. ModelNo: {model[0]}, Width: {model[1]}, Height: {model[2]}, Weight: {model[3]}, Depth: {model[4]}, ScreenSize: {model[5]}")
                else:
                    print('Display ID Not Found.')
            else:
                print("Invalid choice. Returning to main menu.")
        else:
            print("No Digital Displays Found.")
    except Error as e:
        print(f"Error: {e}")

def update_digital_display(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM DigitalDisplay")
        displays = cursor.fetchall()

        if displays:
            print("\nDigital Displays:")
            for i, display in enumerate(displays, start = 1):
                print(f"{i}. SerialNo: {display[0]}, SchedulerSystem: {display[1]}, ModelNo: {display[2]}")

            update = input("\nEnter The Number Corresponding To The Display To Update It, or 'b' to go back: ")

            if update.lower() == 'b':
                return

            if update.isdigit() and 1 <= int(update) <= len(displays):
                serialNo = displays[int(update) - 1][0]
                schedulerSystem = input('Enter Updated Digital Display NEW SchedulerSystem: ')
                modelNo = input('Enter Updated Digital Display NEW ModelNo: ')

                cursor.execute("SELECT modelNo FROM Model WHERE modelNo = %s", (modelNo,))
                model_exists = cursor.fetchall()
                
                if not model_exists:
                    print("\nModel does not exist. Please provide model details. ")
                    width = float(input("Enter model width: "))
                    height = float(input("Enter model height: "))
                    weight = float(input("Enter model weight: "))
                    depth = float(input("Enter model depth: "))
                    screen_size = float(input("Enter model screen_size: "))
                    cursor.execute ("INSERT INTO Model (modelNo, width, height, weight, depth, screenSize) VALUES (%s, %s, %s, %s, %s, %s)",(modelNo, width, height, weight, depth, screen_size))
                    connection.commit()

                cursor.execute('''
                    UPDATE DigitalDisplay
                    SET schedulerSystem = %s, modelNo = %s
                    WHERE serialNo = %s
                    ''', (schedulerSystem, modelNo, serialNo))
                connection.commit()
                print('\nDisplay with SerialNo:', serialNo, 'updated.')

                cursor.execute("SELECT * FROM Model")
                models = cursor.fetchall()
                print("\nModels:")
                for i, model in enumerate(models, start = 1):
                    print(f"{i}. ModelNo: {model[0]}, Width: {model[1]}, Height: {model[2]}, Weight: {model[3]}, Depth: {model[4]}, ScreenSize: {model[5]}")

                cursor.execute("SELECT * FROM DigitalDisplay")
                displays = cursor.fetchall()
                print("\nDigital Displays:")
                for i, display in enumerate(displays, start = 1):
                    print(f"{i}. SerialNo: {display[0]}, SchedulerSystem: {display[1]}, ModelNo: {display[2]}")
            else:
                print("Invalid choice. Returning to main menu.")
        else:
            print("No Digital Displays Found.")
    except Error as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
