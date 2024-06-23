import mysql.connector
from mysql.connector import Error

# Function to connect to database
def create_connection():
    try:
        cnx = mysql.connector.connect(
            user="root", password="215252", host='127.0.0.1' ,database="dogan"
        )
        print("Connection established with the database")
        return cnx
    except mysql.connector.Error as err:
        if err.errno == Error.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == Error.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        cnx.close()
        return None

# Function to execute a query
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
        print(query)
        print("Query executed successfully")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


    
# Insert Operation for Patients
def insert_patients(connection, data):
    query = "INSERT INTO patients (p_id, gender, p_name, contact, bday) VALUES (%s, %s, %s, %s, %s)"
    execute_query(connection, query, data)
    
# Insert Operation for owe_bill
def insert_owe_bill(connection, data):
    query = ("INSERT INTO owe_bill (bill_id, p_id, charges, date) VALUES (%s, %s, %s, %s)")
    execute_query(connection, query, data)

# Function to read data from Patients table
def read_patients(connection):
    query = "SELECT * FROM Patients"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        print(query)
        for record in records:
            print(record)
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Function to read data from Bills table
def read_owe_bills(connection):
    query = "SELECT * FROM owe_bill"
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        print(query)
        for record in records:
            print(record)
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()

# Function to update phone number in Patients table
def update_patient_phone(connection, p_id, new_phone):
    query = "UPDATE Patients SET contact = %s WHERE p_id = %s"
    data = (new_phone, p_id)
    execute_query(connection, query, data)

# Function to update amount in Bills table
def update_bill_amount(connection, bill_id, new_amount):
    query = "UPDATE owe_bill SET charges = %s WHERE bill_id = %s"
    data = (new_amount, bill_id)
    execute_query(connection, query, data)

# Function to delete patient (cascading delete in Bills table)
def delete_patient(connection, patient_id):
    query = "DELETE FROM Patients WHERE p_id = %s"
    data = (patient_id,)
    execute_query(connection, query, data)

# Function to delete bill
def delete_bill(connection, bill_id):
    query = "DELETE FROM owe_bill WHERE bill_id = %s"
    data = (bill_id,)
    execute_query(connection, query, data)

# Main function
def main():

    connection = create_connection()
    cursor = connection.cursor()
    patient_values_to_insert = [

        (23, 'M', 'Dogan Turk', '1234567890', '1985-05-15'),
        (24, 'F', 'Batu Kara', '0987654321', '1990-07-25')
    ]

    bill_values = [

        (23, 11, 100, '2023-04-22'),
        (24, 12, 200, '2023-04-23')
    ]
    # Read and display data before updates
    print("--------------------------------------------------")
    print("Patients before insert:")
    read_patients(connection)
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    print("Bills before insert:")
    read_owe_bills(connection)
    print("--------------------------------------------------")

    
    for patient in patient_values_to_insert:
        insert_patients(connection, patient)

    
    for bill in bill_values:
        insert_owe_bill(connection, bill)
    
        # Read and display data before updates
    print("--------------------------------------------------")
    print("Patients after insert:")
    read_patients(connection)
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    print("Bills after insert:")
    read_owe_bills(connection)
    print("--------------------------------------------------")


        # Read and display data before updates
    print("--------------------------------------------------")
    print("Patients before update:")
    read_patients(connection)
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    print("Bills before update:")
    read_owe_bills(connection)
    print("--------------------------------------------------")

    # Update data
    update_patient_phone(connection, 11, '5555555555')
    update_bill_amount(connection, 23, 151)
    
      # Read and display data before updates
    print("--------------------------------------------------")
    print("Patients after update:")
    read_patients(connection)
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    print("Bills after update:")
    read_owe_bills(connection)
    print("--------------------------------------------------")


    # Delete data
    delete_patient(connection, 23)
    delete_bill(connection,23)
    delete_bill(connection,24)
    # Read and display data after deletions
    print("--------------------------------------------------")
    print("Patients after delete:")
    read_patients(connection)
    print("--------------------------------------------------")
    print("--------------------------------------------------")
    print("Bills after delete:")
    read_owe_bills(connection)
    print("--------------------------------------------------")
     
    
    if connection:
        connection.close()
        print("Connection closed")



main()