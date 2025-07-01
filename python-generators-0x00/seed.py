#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import csv
import uuid

def connect_db():
    """Connect to MySQL server (without database)"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""  # add your MySQL root password here if any
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL server: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if not exists"""
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # your MySQL root password here
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to ALX_prodev: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX idx_user_id(user_id)
    )
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    cursor.close()

def insert_data(connection, csv_file):
    """
    Insert rows from csv_file into user_data table.
    Only insert if user_id does not already exist.
    CSV expected columns: user_id,name,email,age
    """
    cursor = connection.cursor()

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Check if this user_id already exists
            cursor.execute("SELECT 1 FROM user_data WHERE user_id = %s", (row['user_id'],))
            if cursor.fetchone():
                # user_id exists, skip insert
                continue
            
            # Insert new row
            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            data_tuple = (row['user_id'], row['name'], row['email'], row['age'])
            try:
                cursor.execute(insert_query, data_tuple)
            except mysql.connector.Error as err:
                print(f"Error inserting data {data_tuple}: {err}")

    connection.commit()
    cursor.close()
