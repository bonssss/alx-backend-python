#!/usr/bin/python3
import mysql.connector

def streamusersinbatches(batchsize):
    """Generator: yield batches of user_data rows as lists of dicts."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Change if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)

        offset = 0
        while True:
            cursor.execute(
                "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
                (batchsize, offset)
            )
            batch = cursor.fetchall()
            if not batch:
                break
            yield batch
            offset += batchsize

        return  # Optional plain return, does NOT return data

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def batch_processing(batchsize):
    """Generator: yield users over age 25 from batches."""
    for batch in streamusersinbatches(batchsize):
        for user in batch:
            if user['age'] > 25:
                yield user

    return  # Optional plain return, does NOT return data
