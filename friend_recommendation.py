import sqlite3
from prettytable import PrettyTable
import pickle
import os

# Define paths and filenames
dbpath = './dummy_data/'
frpath = './friends_network/'
dbfile = 'dummydata_'
repr_type = 'linked_list'

# Get the size of the database from the user
n_size = int(input("Enter the size of database: "))

# Define the paths for the friends network file and the database file
friend_filename = frpath + repr_type + '_' + dbfile + str(n_size) + '.pkl'
db_filename = dbpath + dbfile + str(n_size) + '.db'


# Function to display rows in a pretty table
def disp_(rows):
    table = PrettyTable(['ID', 'Name', 'DOB', 'Location', 'Company', 'Hobbies'])
    for r in rows:
        table.add_row(r)
    print(table)


# Load the friends network representation
if not os.path.exists(friend_filename):
    print(f"Friend file {friend_filename} does not exist. Please create the friends network first.")
    exit()

with open(friend_filename, 'rb') as f:
    friend_repr = pickle.load(f)

# Get user input with default values
print("Press Enter for default.")
Name = input("Input Name: ").strip()
DOB = input('Input Year of Birth (1975 - 2010): ').strip()
Location = input("Input your Location. Major Cities from India ('Delhi','Bangalore','Mumbai','Hyderabad','Pune'): ").strip().lower()
Company = input("Input your Company. Top 10 Companies from World:( 'Apple', 'Google', 'Amazon','Microsoft'): ").strip().lower()
Hobbies = input("Input your Hobbies. Space separated:('Sports', 'Music', 'Dance', 'Reading', 'Gaming'): ").strip().lower()

if Name == '':
    Name = 'Yash Gupta'
if DOB == '':
    DOB = '1998'
if Location == '':
    Location = 'delhi'
if Company == '':
    Company = 'google'
if Hobbies == '':
    Hobbies = 'gaming'

print(Name, DOB, Location, Company, Hobbies)

# Connect to the database
try:
    conn = sqlite3.connect(db_filename)
    print("Open database successfully")
except sqlite3.Error as e:
    print(f"Failed to open database: {e}")
    exit()

# Query the database based on user input
curr = conn.cursor()
curr.execute("SELECT * FROM Data WHERE lower(Location)=? AND lower(Company)=?", (Location, Company))
rows = curr.fetchall()
curr.close()

# Display the queried data
disp_(rows)

# Initialize the friend list
friend_list = [300, 250]

while True:
    print("Enter ID of the person to become friend")
    print("Enter 0 to view current list of friends")
    new_friend = int(input())

    if new_friend == 0:
        print(friend_list)
        curr = conn.cursor()
        query = "SELECT * FROM Data WHERE ID IN ({seq})".format(seq=','.join(['?'] * len(friend_list)))
        curr.execute(query, friend_list)
        rows = curr.fetchall()
        curr.close()
        disp_(rows)
    else:
        if new_friend not in friend_list:
            friend_list.append(new_friend)

        all_recommendations = []
        for i in friend_list:
            for j in friend_repr[int(i) - 1]:
                curr = conn.cursor()
                curr.execute("SELECT ID FROM Data WHERE ID=? AND lower(Hobbies) LIKE ?", (j, '%' + Hobbies + '%'))
                rows = curr.fetchall()
                rows_list = [r[0] for r in rows]
                curr.close()
                all_recommendations.extend(rows_list)

        all_recommendations = list(set(all_recommendations))  # Remove duplicates
        print(all_recommendations)
        if all_recommendations:
            curr = conn.cursor()
            query = "SELECT * FROM Data WHERE ID IN ({seq})".format(seq=','.join(['?'] * len(all_recommendations)))
            curr.execute(query, all_recommendations)
            rows = curr.fetchall()
            curr.close()
            disp_(rows)
