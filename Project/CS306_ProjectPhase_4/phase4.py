from pymongo import MongoClient
from pymongo import errors
import certifi
from bson import ObjectId  # Import ObjectId from bson module

def connectDB():
    try:
        connection_string = "mongodb+srv://hospitaltest:hospitaltest@cluster0.nrwmeoa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = MongoClient(connection_string, tlsCAFile=certifi.where())

        db = client.cluster0
        print("Connection established to your db")
        return db

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

def createCollection(db, collection_name):
    try:
        # If the collection doesn't exist, create it
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        else:
            print("Collection already exists")
    except Exception as e:
        print("An error occurred: ", e)

def insert_into_collection(db, collection_name, data, p_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        query = {"p_id": p_id}

        # Check if the patient already exists
        existing_patient = collection.find_one(query)

        if existing_patient:
            # Append the new review to the existing reviews array
            update = {"$push": {"reviews": data}}
            result = collection.update_one(query, update)
            print("Update successfully completed")
        else:
            # Insert a new document with the initial review
            new_patient_data = {"p_id": p_id, "reviews": [data]}
            result = collection.insert_one(new_patient_data)
            print("Insertion successfully completed")
            print(f"Inserted document ID: {result.inserted_id}")

    except Exception as e:
        print(f"An error occurred: {e}")

def read_all_data(db, collection_name):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Use the find method to retrieve all documents
        result = collection.find()

        # Iterate through the documents and print them
        for document in result:
            print(document)

    except Exception as e:
        print(f"An error occurred: {e}")


from bson import ObjectId

# Read data with filtering
def read_filtered_data(db, collection_name):

    collection = db[collection_name]

    # Display all possible top-level keys
    example_document = collection.find_one()
    all_keys = list(example_document.keys())

    print("Available top-level fields:")
    print(all_keys)

    filter_key = input("Enter the field to filter: ")
    filter_value = input("Enter the criteria value to read: ")
    # like that reviews.patient_reviews.doctor_name
    # Create a filter query for nested fields
    def create_nested_filter_query(filter_key, filter_value):
        keys = filter_key.split('.')
        query = {keys[0]: {'$elemMatch': {keys[1]: {'$elemMatch': {keys[2]: filter_value}}}}}
        return query

    if '.' in filter_key:
        filter_query = create_nested_filter_query(filter_key, filter_value)
    else:
        filter_query = {filter_key: filter_value}

    for document in collection.find(filter_query):
        print(document)


"""

def find_orders_containing_item(db, collection_name, item_value):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find orders containing the specified item
        query = {"DoctorReviews.doctor_name": item_value}

        # Use the find method to retrieve matching documents
        cursor = collection.find(query)

        # Convert your cursor to a list to freely operate over it
        result = list(cursor)

        # Print the matching documents
        for document in result:
            print(document)

        # Return the whole result list
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
"""

def update_hospital_review_by_pid_and_date(db, collection_name, p_id, review_date, new_review, new_rate):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the specific review to update
        query = {
            "p_id": p_id,
            "reviews.patient_reviews": {
                "$elemMatch": {
                    "review_date": review_date
                }
            }
        }

        # Define the update operation to set the new review and rate
        update = {
            "$set": {
                "reviews.$[reviewElement].patient_reviews.$[patientElement].review": new_review,
                "reviews.$[reviewElement].patient_reviews.$[patientElement].rate": new_rate
            }
        }

        # Define array filters to match the correct nested document
        array_filters = [
            {"reviewElement.patient_reviews": {"$exists": True}},
            {"patientElement.review_date": review_date}
        ]

        # Use the update_many method to update the review and rate
        result = collection.update_many(query, update, array_filters=array_filters)

        # Check if any documents were updated
        if result.modified_count >= 1:
            print(f"Successfully updated the review and rate for p_id {p_id} with review date {review_date} in {result.modified_count} record(s)")
        else:
            print(f"No records found with p_id {p_id} and review date {review_date}")

        # Return the result for further processing if needed
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def delete_record_by_id(db, collection_name, p_id):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the document by its ID
        query = {"p_id": p_id}

        # Use the delete_one method to delete the document
        result = collection.delete_one(query)

        # Check if the deletion was successful
        if result.deleted_count == 1:
            print(f"Successfully deleted record with ID {p_id}")
        else:
            print(f"No record found with ID {p_id}")

    except errors.PyMongoError as e:
        print(f"An error occurred: {e}")

def update_review_by_doctor_and_time(db, collection_name, d_name, appointment_time, new_review):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the specific review to update
        query = {
            "reviews.patient_reviews": {
                "$elemMatch": {
                    "doctor_name": d_name,
                    "appointment_time": appointment_time
                }
            }
        }

        # Define the update operation to set the new review
        update = {
            "$set": {
                "reviews.$[reviewElement].patient_reviews.$[patientElement].review": new_review
            }
        }

        # Define array filters to match the correct nested document
        array_filters = [
            {"reviewElement.patient_reviews": {"$exists": True}},
            {"patientElement.doctor_name": d_name, "patientElement.appointment_time": appointment_time}
        ]

        # Use the update_many method to update the review
        result = collection.update_many(query, update, array_filters=array_filters)

        # Check if any documents were updated
        if result.modified_count >= 1:
            print(f"Successfully updated the review for doctor {d_name} with appointment time {appointment_time} in {result.modified_count} record(s)")
        else:
            print(f"No records found with doctor name {d_name} and appointment time {appointment_time}")
            
        # Return the result for further processing if needed
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def delete_hospital_review_by_pid_and_date(db, collection_name, p_id, review_date):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the query to find the specific review to delete
        query = {
            "p_id": p_id,
            "reviews.patient_reviews.review_date": review_date
        }

        # Define the update operation to pull the review with the specified review date
        update = {
            "$pull": {
                "reviews.$[].patient_reviews": {"review_date": review_date}
            }
        }

        # Execute the update operation
        result = collection.update_many(query, update)

        if result.modified_count >= 1:
            print(f"Successfully removed the review for p_id {p_id} with review date {review_date} from {result.modified_count} record(s)")
        else:
            print(f"No records found with p_id {p_id} and review date {review_date}")

        # Return the result for further processing if needed
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def delete_reviews_by_doctorname(db, collection_name, d_name):
    try:
        # Access the specified collection
        collection = db[collection_name]

        # Define the update operation to pull the review with the specified doctor name
        update = {
            "$pull": {
                "reviews.$[].patient_reviews": {"doctor_name": d_name}
            }
        }

        # Execute the update operation
        result = collection.update_many({}, update)

        if result.modified_count >= 1:
            print(f"Successfully removed reviews by {d_name} from {result.modified_count} record(s)")
        else:
            print(f"No records found with doctor name {d_name}")

        # Return the result for further processing if needed
        return result

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # First create a connection
    db = connectDB()

    mylist = ["DoctorReviews","HospitalReviews"]
    print("Welcome to Review Portal!")
    p_id = input("Please enter your patient id:")
    print("Please pick the option that you want to proceed.")
    option = 0
    while(option != 7):
        print("\n1 - Create a collection.")
        print("2 - Read all data in a collection.")
        print("3 - Read some part of the data while filtering.")
        print("4 - Insert data.")
        print("5 - Delete data.")
        print("6 - Update data.")
        print("7 - Exit.")
        option = int(input("Selected option: "))

        if option == 7:
            break
            
        if option == 1:
            collection_name = input("Enter the collection name: ")
            createCollection(db, collection_name)

        elif option == 2:
            collection_name = input("Please enter the collection name to read: ")
            read_all_data(db, collection_name)

        elif option == 3:
            collection_name = input("Enter the collection name: ")
            #filter_field = input("Enter the field to filter by: ")
            #filter_value = input("Enter the value to filter by: ")
            #find_orders_containing_item(db, collection_name, filter_field, filter_value)
            read_filtered_data(db, collection_name)

        elif option == 4:
            print("Please select the collection you want to insert data: ")
            for i in range(0, len(mylist)):
                print(i+1, "- ", mylist[i])
            print()
            collection_option = int(input("Selected option: "))
            data = {}
            lastdata = {}
            if collection_option == 1:
                print("Please enter the data fields:\n")
                info = []
                d_name = input("doctor_name:")
                data["doctor_name"] = d_name
                app_time = input("appointment_time:")
                data["appointment_time"] = app_time
                review = input("review:")
                data["review"] = review
                info.append(data)
                lastdata["patient_reviews"] = info
                print()
                print(lastdata)
                insert_into_collection(db, mylist[collection_option-1], lastdata, p_id)
            
            if collection_option == 2:
                print("Please enter the data fields:\n")
                info = []
                rate = input("rate:")
                data["rate"] = rate
                app_time = input("visit_date:")
                data["review_date"] = app_time
                review = input("review:")
                data["review"] = review
                info.append(data)
                lastdata["patient_reviews"] = info
                print()
                print(lastdata)
                insert_into_collection(db, mylist[collection_option-1], lastdata, p_id)

        elif option == 5:
            print("Please select the collection you want to delete data: ")
            for i in range(0, len(mylist)):
                print(i+1, "- ", mylist[i])
            print()
            collection_option = int(input("Selected option: "))
            if collection_option == 1:
                n = int(input("Delete option to according to id(0) or doctor name (1):"))
                if n == 0:
                    p_id_new = input("Enter p_id to delete:")
                    delete_record_by_id(db, mylist[collection_option-1], p_id_new)
                if n == 1:
                    d_name = input("Enter doctor name to delete:")
                    delete_reviews_by_doctorname(db, mylist[collection_option-1], d_name)
            
            if collection_option == 2:
                n = int(input("Delete option to according to id(0) or review_date (1):"))
                if n == 0:
                    p_id_new = input("Enter p_id to delete:")
                    delete_record_by_id(db, mylist[collection_option-1], p_id_new)
                if n == 1:
                    review_date = input("Enter the review date: ")
                    delete_hospital_review_by_pid_and_date(db, mylist[collection_option-1], p_id, review_date)
                    
        elif option == 6:
            print("Please select the collection you want to update data: ")
            for i in range(0, len(mylist)):
                print(i+1, "- ", mylist[i])
            print()
            collection_option = int(input("Selected option: "))

            if collection_option == 1:
                doctor_name = input("Enter the Doctor name: ")
                appointment_time = input("Enter the appointment time: ")
                new_review = input("Enter the new review: ")
                update_review_by_doctor_and_time(db, mylist[collection_option-1], doctor_name, appointment_time, new_review)
            
            if collection_option == 2:
                review_date = input("Enter the review date: ")
                new_review = input("Enter the new review: ")
                new_rate = input("Enter the new rate: ")
                update_hospital_review_by_pid_and_date(db, mylist[collection_option-1], p_id, review_date, new_review, new_rate)

        else:
            print("Invalid option, please try again.")