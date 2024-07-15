import sqlite3
import names
import random
from random import sample
from os import path, makedirs

# Predefined lists for data generation
Company = ['Microsoft', 'Samsung', 'Toyota', 'Facebook', 'Apple', 'Google', 'Amazon']
DOB = [ '2000', '1995', '1990', '1985', '1980', '1975', '1970','1998', '1994', '1993']
Location = ['Delhi', 'Bangalore', 'Mumbai', 'Kolkata', 'Hyderabad', 'Pune', 'Jaipur', 'Goa', 'Chennai']
Hobbies = ['Sports', 'Music', 'Dance', 'Reading', 'Gaming', 'Craft', 'Travel', 'Fishing', 'Acting', 'Gardening']


# Connect to Database using sqlite3
def connectdb(database):
    '''
    Input: String
    Output: sqlite3.Connection
    '''
    try:
        conn = sqlite3.connect(database)
        print("Open database successfully")
        return conn
    except sqlite3.Error as e:
        print(f"Failed to open database: {e}")


def createtable(conn):
    '''
    Input: sqlite3.Connection
    Output: Create the Table in the database
    '''
    curr = conn.cursor()
    try:
        curr.execute('''CREATE TABLE Data (
            ID INTEGER PRIMARY KEY, 
            Name TEXT NOT NULL,
            DOB TEXT NOT NULL,
            Location TEXT NOT NULL,
            Company TEXT NOT NULL,
            Hobbies TEXT NOT NULL)''')
        print("Table created successfully")
    except sqlite3.Error as e:
        print(f"Failed to create table: {e}")
    conn.commit()


def inserttable(database, n_size):
    '''
    Input: database, size of database
    Output: Insert the table with data
    '''
    con = sqlite3.connect(database)
    try:
        for i in range(n_size):
            curr = con.cursor()
            entry = (
                i + 1,
                names.get_full_name(),
                random.choice(DOB),
                random.choice(Location),
                random.choice(Company),
                ' '.join(sample(Hobbies, random.choice([1, 2, 3, 4])))
            )
            curr.execute("INSERT INTO Data (ID, Name, DOB, Location, Company, Hobbies) VALUES (?, ?, ?, ?, ?, ?)",
                         entry)
            curr.close()
        con.commit()
    except sqlite3.Error as e:
        print(f"Failed to insert data: {e}")
        con.rollback()
    finally:
        con.close()


# Driver program
def main():
    '''
    Output: Creates the database with title - "dummydata_x" + where x represents number of datapoints.
    '''
    # Data is set limited to 1000 points to avoid generating similar data.
    while True:
        try:
            n_size = int(input("Please select size of database between 100 and 1000: "))
            # Check limits
            if 100 <= n_size <= 1000:
                break
            else:
                print("Please enter a number between 100 and 1000.")
        except ValueError:
            print("Invalid input. Please enter a number between 100 and 1000.")

    # Database path
    database = f"./dummy_data/dummydata_{n_size}.db"
    print("Database is", database)

    # Check if the database already exists
    if not path.exists(database):
        # Create directory if it does not exist
        if not path.exists("./dummy_data"):
            makedirs("./dummy_data")
        # Connect to database
        conn = connectdb(database)
        # Create Table
        createtable(conn)
        # Insert data into Table
        inserttable(database, n_size)
    else:
        print("Database already exists.")


# Call the main function
if __name__ == "__main__":
    main()
