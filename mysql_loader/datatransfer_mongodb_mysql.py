import pymongo
import mysql.connector
import time

mysql_host = "mysql-service"
mysql_user = "admin"
mysql_password = "admin"
mysql_database = "hogwarts"

mongodb_host = "mongodb-service"
mongodb_port = 27017
mongodb_database = "hogwarts"
mongodb_client = pymongo.MongoClient(mongodb_host, mongodb_port)
mongodb_db = mongodb_client[mongodb_database]
col_spells = mongodb_db["Spells"]
col_characters = mongodb_db["Characters"]

print("Data successfully retrieved from MongoDB.")
print("Waiting for 15 seconds before starting MySQL operations...")
time.sleep(15)

def transfer_data_to_mysql(mongo_collection, mysql_table):
    mongo_data = list(mongo_collection.find())
    conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database
    )
    cursor = conn.cursor()
    cursor.execute(f"TRUNCATE TABLE {mysql_table}")

    for record in mongo_data:
        if mysql_table == "Spells":
            values = (record.get('name'), record.get('description'))
            sql = "INSERT INTO Spells (name, description) VALUES (%s, %s)"
        elif mysql_table == "Characters":
            values = (
                record.get('name'), record.get('species'), record.get('gender'), 
                record.get('house'), record.get('dateOfBirth'), record.get('yearOfBirth'), 
                int(record.get('wizard', False)), record.get('ancestry'), 
                record.get('eyeColour'), record.get('hairColour'), record.get('patronus'), 
                int(record.get('hogwartsStudent', False)), int(record.get('hogwartsStaff', False)), 
                record.get('actor'), int(record.get('alive', False)), record.get('image')
            )
            sql = "INSERT INTO Characters (name, species, gender, house, dateOfBirth, yearOfBirth, wizard, ancestry, eyeColour, hairColour, patronus, hogwartsStudent, hogwartsStaff, actor, alive, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(sql, values)
        delete_duplicates_query = f"""
            DELETE t1
            FROM {mysql_table} t1
            INNER JOIN {mysql_table} t2
            WHERE t1.id < t2.id
            AND t1.name = t2.name
        """

        cursor.execute(delete_duplicates_query)
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data transfer to {mysql_table} complete.")

print("Waiting for 15 seconds...")
time.sleep(15)

print("Transferring Spells data...")
transfer_data_to_mysql(col_spells, "Spells")
print("Transferring Characters data...")
transfer_data_to_mysql(col_characters, "Characters")
print("Data transfer to MySQL complete.")