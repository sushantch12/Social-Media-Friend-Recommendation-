import random
import sqlite3
import pickle
import os

linked_list_representation = []

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
        print("Invalid input. Please enter a valid number.")

# Make the initial friends
path = './dummy_data/'
dbfile = 'dummydata_'

database = path + dbfile + str(n_size) + ".db"

# Check if the database exists
if not os.path.exists(database):
    print(f"Database {database} does not exist. Please create the database first.")
else:
    conn = sqlite3.connect(database)
    curr = conn.cursor()
    curr.execute('SELECT COUNT(*) FROM Data')
    rows = curr.fetchone()
    no_of_people = rows[0]
    conn.commit()

    all_people = [int(i) for i in range(1, no_of_people + 1)]

    min_friends = 50
    max_friends = 100
    poss_friend = [int(i) for i in range(min_friends, max_friends)]

    for i in all_people:
        # assuming each person has 50-99 friends
        temp_choice = random.sample(all_people, random.choice(poss_friend))
        temp_choice.sort()
        try:
            temp_choice.remove(i)
        except ValueError:
            pass
        linked_list_representation.append(temp_choice)

    # Ensure the directory exists
    save_path = './friends_network/'
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    save_filename = save_path + 'linked_list_' + dbfile + str(n_size) + '.pkl'

    with open(save_filename, 'wb') as f:
        pickle.dump(linked_list_representation, f)

    print(f"Friends network saved to {save_filename}")
