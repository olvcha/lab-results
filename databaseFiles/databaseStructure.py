import sqlite3


class DatabaseStructure:
    # Connect to the SQLite database file
    conn = sqlite3.connect('labResults.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Fetch all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print the names of all tables
    print("Tables in the database:")
    for table in tables:
        print(table[0])

    # Now fetch and display the structure of each table and retrieve all data
    for table in tables:
        table_name = table[0]

        # Print structure of the current table
        print(f"\nStructure of table '{table_name}':")
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Print column details for the table
        print(f"{'Column ID':<10} {'Name':<20} {'Type':<15} {'NotNull':<10} {'Default':<10} {'Primary Key':<10}")
        for column in columns:
            col_id = column[0] if column[0] is not None else 'N/A'
            name = column[1] if column[1] is not None else 'N/A'
            col_type = column[2] if column[2] is not None else 'N/A'
            not_null = column[3] if column[3] is not None else 'N/A'
            default = column[4] if column[4] is not None else 'N/A'
            primary_key = column[5] if column[5] is not None else 'N/A'

            print(f"{col_id:<10} {name:<20} {col_type:<15} {not_null:<10} {default:<10} {primary_key:<10}")

        # Fetch and print all data from the current table
        print(f"\nData in table '{table_name}':")
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        if rows:
            # Print header
            headers = [description[0] for description in cursor.description]
            print(f"{' | '.join(headers)}")

            # Print each row
            for row in rows:
                print(f"{' | '.join(str(item) for item in row)}")
        else:
            print("No data found.")

    # Close the connection
    conn.close()
