import json
import pymongo
import mysql.connector

# MongoDB connection settings
mongodb_host = "mongodb-container"
mongodb_port = 27017
mongodb_database = "hogwarts"
mongodb_collection = "stuff"

# MySQL connection settings
mysql_host = "mysql-container"
mysql_user = "admin"
mysql_password = "admin"
mysql_database = "hogwarts"

# Connect to MongoDB
mongodb_client = pymongo.MongoClient(mongodb_host, mongodb_port)
mongodb_db = mongodb_client[mongodb_database]
mongodb_collection = mongodb_db[mongodb_collection]

# Connect to MySQL
mysql_connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)
mysql_cursor = mysql_connection.cursor()

# ETL Process
try:
    # Extract data from MongoDB
    mongo_data = mongodb_collection.find()
    print("mongo_data: ", mongo_data)

    # Transform and load data into MySQL
    for document in mongo_data:
        # Define your transformation logic here if needed
        id = document.get("id")
        name = document.get("name")
        description = document.get("description")

        # Prepare SQL query
        insert_query = "INSERT INTO Characters (id, name, description) VALUES (%s, %s, %s)"
        values = (id, name, description)

        # Execute the query
        mysql_cursor.execute(insert_query, values)
    
    # Commit changes to MySQL
    mysql_connection.commit()
    print("Data loaded into MySQL successfully.")

except Exception as e:
    print(f"Error: {e}")
finally:
    # Close MongoDB and MySQL connections
    mongodb_client.close()
    mysql_cursor.close()
    mysql_connection.close()
