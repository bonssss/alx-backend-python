#!/usr/bin/python3
import mysql.connector

def stream_user_ages():
    """
    Generator that yields user ages one by one from user_data table.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # update if needed
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row['age']
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def calculate_average_age():
    """
    Uses stream_user_ages generator to compute average age without loading all data at once.
    """
    total_age = 0
    count = 0
    for age in stream_user_ages():
        total_age += age
        count += 1

    average = total_age / count if count > 0 else 0
    print(f"Average age of users: {average}")

if __name__ == "__main__":
    calculate_average_age()
