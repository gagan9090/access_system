import sqlite3

def view_database():
    conn = sqlite3.connect('system_usage.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usage')
    rows = cursor.fetchall()
    conn.close()

    # Display the data
    if rows:
        print("Date | Boot Time | Shutdown Time | Most Used App")
        print("-" * 50)
        for row in rows:
            print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}")
    else:
        print("No data found in the database.")

view_database()
