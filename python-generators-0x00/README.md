# Python Generators Project - ALX Backend Prodev

## Overview

This project demonstrates working with Python generators and MySQL databases by creating and populating a database, then streaming database rows one by one using a Python generator.

## Features

- Connect to MySQL server
- Create a database `ALX_prodev` if it doesn't exist
- Create a `user_data` table with fields:
  - `user_id` (UUID string, Primary Key, Indexed)
  - `name` (string, NOT NULL)
  - `email` (string, NOT NULL)
  - `age` (decimal, NOT NULL)
- Insert data from a CSV file (`user_data.csv`) into the table, ignoring duplicates by `user_id`
- Provide a generator function to stream rows one at a time from the `user_data` table

## File Structure

