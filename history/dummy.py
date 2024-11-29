import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('university.db')
cursor = conn.cursor()

# Retrieve data from a specific table, e.g., 'user_detail'
cursor.execute("SELECT * FROM user_detail;")
data = cursor.fetchall()

# Display the retrieved data
for row in data:
    print(row)

# Close the connection
conn.close()
