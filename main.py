import mysql.connector
import logging

# Logging configuration
logging.basicConfig(filename="employee_management.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


# Database connection function with exception handling
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="tiger",
            database="company"
        )
        if connection.is_connected():
            logging.info("Connected to the database")
            return connection
    except mysql.connector.Error as e:
        logging.error(f"Error: {e}")
        print("Failed to connect to the database.")
        return None


# Validate inputs for employee data
def validate_input(prompt, input_type):
    while True:
        try:
            if input_type == "int":
                value = int(input(prompt))
                if value <= 0:
                    raise ValueError
            elif input_type == "float":
                value = float(input(prompt))
                if value <= 0:
                    raise ValueError
            else:
                value = input(prompt)
            return value
        except ValueError:
            print("Invalid input. Please try again.")


# Create employee
def create_employee(connection):
    name = input("Enter employee name: ")
    age = validate_input("Enter employee age (positive integer): ", "int")
    department = input("Enter employee department: ")
    salary = validate_input("Enter employee salary (positive number): ", "float")

    cursor = connection.cursor()
    query = "INSERT INTO employees (name, age, department, salary) VALUES (%s, %s, %s, %s)"
    data = (name, age, department, salary)

    try:
        cursor.execute(query, data)
        connection.commit()
        logging.info(f"Employee '{name}' added successfully")
        print("Employee added successfully!")
    except mysql.connector.Error as e:
        logging.error(f"Failed to insert into MySQL table: {e}")
        print("Failed to add employee.")


# Read employees with pagination
def read_employees(connection, page_size=5):
    cursor = connection.cursor()
    query = "SELECT * FROM employees"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
        total_records = len(result)
        pages = (total_records // page_size) + (1 if total_records % page_size != 0 else 0)

        current_page = 1
        while current_page <= pages:
            start = (current_page - 1) * page_size
            end = start + page_size
            print(f"\n--- Employees Page {current_page} ---")
            for row in result[start:end]:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Department: {row[3]}, Salary: {row[4]}")

            if current_page < pages:
                next_page = input("Press Enter to view next page or type 'exit' to quit: ").strip().lower()
                if next_page == 'exit':
                    break

            current_page += 1

    except mysql.connector.Error as e:
        logging.error(f"Failed to retrieve data: {e}")
        print("Error retrieving employee data.")


# Search employees by name or department
def search_employee(connection):
    search_term = input("Enter the employee's name or department to search: ")
    cursor = connection.cursor()
    query = "SELECT * FROM employees WHERE name LIKE %s OR department LIKE %s"
    data = (f"%{search_term}%", f"%{search_term}%")

    try:
        cursor.execute(query, data)
        result = cursor.fetchall()

        if result:
            print("\n--- Search Results ---")
            for row in result:
                print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Department: {row[3]}, Salary: {row[4]}")
        else:
            print("No matching records found.")

    except mysql.connector.Error as e:
        logging.error(f"Failed to search employees: {e}")
        print("Error searching employees.")


# Update employee
def update_employee(connection):
    employee_id = validate_input("Enter the ID of the employee you want to update: ", "int")

    print("\nEnter the new details (leave blank to keep unchanged):")
    name = input("New name: ")
    age = input("New age: ")
    department = input("New department: ")
    salary = input("New salary: ")

    cursor = connection.cursor()
    query = "UPDATE employees SET "
    fields = []
    data = []

    if name:
        fields.append("name = %s")
        data.append(name)
    if age:
        fields.append("age = %s")
        data.append(int(age))
    if department:
        fields.append("department = %s")
        data.append(department)
    if salary:
        fields.append("salary = %s")
        data.append(float(salary))

    if fields:
        query += ", ".join(fields) + " WHERE id = %s"
        data.append(employee_id)
        try:
            cursor.execute(query, tuple(data))
            connection.commit()
            logging.info(f"Employee ID {employee_id} updated successfully")
            print("Employee updated successfully!")
        except mysql.connector.Error as e:
            logging.error(f"Failed to update employee: {e}")
            print("Failed to update employee.")
    else:
        print("No changes were made.")


# Delete employee
def delete_employee(connection):
    employee_id = validate_input("Enter the ID of the employee you want to delete: ", "int")

    cursor = connection.cursor()
    query = "DELETE FROM employees WHERE id = %s"

    try:
        cursor.execute(query, (employee_id,))
        connection.commit()
        logging.info(f"Employee ID {employee_id} deleted successfully")
        print("Employee deleted successfully!")
    except mysql.connector.Error as e:
        logging.error(f"Failed to delete employee: {e}")
        print("Failed to delete employee.")


# Main function with advanced features and search functionality
def main():
    connection = connect_to_db()

    if connection:
        while True:
            print("\n--- Employee Management System ---")
            print("1. Create Employee")
            print("2. Read Employees")
            print("3. Update Employee")
            print("4. Delete Employee")
            print("5. Search Employee")
            print("6. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                create_employee(connection)
            elif choice == '2':
                read_employees(connection)
            elif choice == '3':
                update_employee(connection)
            elif choice == '4':
                delete_employee(connection)
            elif choice == '5':
                search_employee(connection)
            elif choice == '6':
                print("Exiting the system.")
                logging.info("Exiting the Employee Management System.")
                break
            else:
                print("Invalid choice! Please try again.")

        connection.close()


if __name__ == "__main__":
    main()
