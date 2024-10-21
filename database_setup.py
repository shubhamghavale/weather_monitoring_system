import sqlite3

def setup_database():
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        temp REAL NOT NULL,
                        feels_like REAL NOT NULL,
                        main TEXT NOT NULL,
                        timestamp INTEGER NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_summary (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT NOT NULL,
                        avg_temp REAL NOT NULL,
                        max_temp REAL NOT NULL,
                        min_temp REAL NOT NULL,
                        dominant_condition TEXT NOT NULL,
                        date TEXT NOT NULL
                    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
