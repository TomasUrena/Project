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
                print("2. Logout")

                choice = input("\nEnter your choice: ")

                if choice == '1':
                    display_digital_displays(connection)
                elif choice == '2':
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


if __name__ == "__main__":
    main()
