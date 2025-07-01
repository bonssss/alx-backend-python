#!/usr/bin/python3
import mysql.connector

def stream_users():
    """Generator function that yields rows one by one from user_data as dicts"""
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Update if your MySQL password is different
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)  # dictionary=True to get dict results
        cursor.execute("SELECT user_id, name, email, age FROM user_data")

        # Loop once, yield each row as dict
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
