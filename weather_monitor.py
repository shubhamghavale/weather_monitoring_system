import sqlite3
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
SIMULATION_DAYS = 7  # Number of days to simulate
THRESHOLD_TEMP = 35  # Example: 35°C

# Simulated weather conditions
WEATHER_CONDITIONS = ['Clear', 'Clouds', 'Rain', 'Drizzle', 'Thunderstorm']

def generate_mock_weather_data(city, days=SIMULATION_DAYS):
    """
    Generate mock weather data for the given city over several days, including additional parameters.
    """
    weather_data = []
    current_time = datetime.now()

    for day in range(days):
        temp = random.uniform(20, 45)  # Generate random temperature between 20 and 45°C
        feels_like = temp + random.uniform(-2, 2)  # Feels like temperature variation
        humidity = random.uniform(30, 90)  # Simulated humidity between 30% and 90%
        wind_speed = random.uniform(1, 15)  # Simulated wind speed between 1 and 15 m/s
        main_condition = random.choice(WEATHER_CONDITIONS)  # Random weather condition
        timestamp = current_time - timedelta(days=day)

        weather_data.append({
            'city': city,
            'temp': temp,
            'feels_like': feels_like,
            'humidity': humidity,  # Added humidity
            'wind_speed': wind_speed,  # Added wind speed
            'main': main_condition,
            'timestamp': timestamp
        })

    return weather_data

def store_weather_data(data):
    """
    Store the simulated weather data in the SQLite database.
    """
    conn = sqlite3.connect('weather_simulation.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                        city TEXT, 
                        temp REAL, 
                        feels_like REAL, 
                        humidity REAL,
                        wind_speed REAL,
                        main TEXT, 
                        timestamp TEXT)''')

    # Add new columns if they don't exist (for backward compatibility)
    try:
        cursor.execute('''ALTER TABLE weather ADD COLUMN humidity REAL''')
    except sqlite3.OperationalError:
        # Ignore if the column already exists
        pass

    try:
        cursor.execute('''ALTER TABLE weather ADD COLUMN wind_speed REAL''')
    except sqlite3.OperationalError:
        # Ignore if the column already exists
        pass

    # Insert the weather data
    for entry in data:
        cursor.execute('''INSERT INTO weather (city, temp, feels_like, humidity, wind_speed, main, timestamp)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                          (entry['city'], entry['temp'], entry['feels_like'], entry['humidity'], entry['wind_speed'], entry['main'], entry['timestamp']))
    
    conn.commit()
    conn.close()


def rollup_daily_summary():
    """
    Create daily summaries for each city, including average humidity and max wind speed.
    """
    conn = sqlite3.connect('weather_simulation.db')
    cursor = conn.cursor()

    # Create table for daily summary if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS daily_summary (
                        city TEXT, 
                        avg_temp REAL, 
                        max_temp REAL, 
                        min_temp REAL, 
                        avg_humidity REAL,
                        max_wind_speed REAL,
                        dominant_condition TEXT, 
                        date TEXT)''')

    # Add new columns if they don't exist (for backward compatibility)
    try:
        cursor.execute('''ALTER TABLE daily_summary ADD COLUMN avg_humidity REAL''')
    except sqlite3.OperationalError:
        pass  # Ignore if column already exists

    try:
        cursor.execute('''ALTER TABLE daily_summary ADD COLUMN max_wind_speed REAL''')
    except sqlite3.OperationalError:
        pass  # Ignore if column already exists

    for city in CITIES:
        cursor.execute('''SELECT DATE(timestamp), AVG(temp), MAX(temp), MIN(temp), AVG(humidity), MAX(wind_speed), main, COUNT(main)
                          FROM weather
                          WHERE city = ?
                          GROUP BY DATE(timestamp), main
                          ORDER BY DATE(timestamp), COUNT(main) DESC''', (city,))
        results = cursor.fetchall()

        for result in results:
            date, avg_temp, max_temp, min_temp, avg_humidity, max_wind_speed, dominant_condition, _ = result
            cursor.execute('''INSERT INTO daily_summary (city, avg_temp, max_temp, min_temp, avg_humidity, max_wind_speed, dominant_condition, date)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                           (city, avg_temp, max_temp, min_temp, avg_humidity, max_wind_speed, dominant_condition, date))
            conn.commit()

    conn.close()


def visualize_daily_summary():
    """
    Generate separate graphs for each city showing max, min, and average temperatures, 
    humidity, and wind speed over the simulation period.
    """
    conn = sqlite3.connect('weather_simulation.db')
    cursor = conn.cursor()

    for city in CITIES:
        cursor.execute('''SELECT date, avg_temp, max_temp, min_temp, avg_humidity, max_wind_speed 
                          FROM daily_summary WHERE city = ? ORDER BY date''', (city,))
        data = cursor.fetchall()

        if data:
            dates = [row[0] for row in data]
            avg_temps = [row[1] for row in data]
            max_temps = [row[2] for row in data]
            min_temps = [row[3] for row in data]
            avg_humidity = [row[4] for row in data]
            max_wind_speed = [row[5] for row in data]

            # Convert string dates to datetime objects for better plotting
            dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]

            # Plot temperature
            plt.figure(figsize=(10, 6))
            plt.plot(dates, avg_temps, label='Avg Temp', color='blue', marker='o', linestyle='-')
            plt.plot(dates, max_temps, label='Max Temp', color='red', marker='x', linestyle='--')
            plt.plot(dates, min_temps, label='Min Temp', color='green', marker='s', linestyle='-.')
            
            plt.title(f"Daily Temperature Summary for {city}", fontsize=14)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Temperature (°C)', fontsize=12)
            
            # Format date on x-axis for better readability
            plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)

            plt.legend(loc='upper right')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()  # Adjust layout so nothing overlaps

            # Show the temperature plot
            plt.show()

            # Plot humidity
            plt.figure(figsize=(10, 6))
            plt.plot(dates, avg_humidity, label='Avg Humidity (%)', color='purple', marker='o', linestyle='-')
            plt.title(f"Daily Humidity Summary for {city}", fontsize=14)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Humidity (%)', fontsize=12)
            plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)
            plt.legend(loc='upper right')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()

            # Show the humidity plot
            plt.show()

            # Plot wind speed
            plt.figure(figsize=(10, 6))
            plt.plot(dates, max_wind_speed, label='Max Wind Speed (m/s)', color='orange', marker='x', linestyle='--')
            plt.title(f"Daily Wind Speed Summary for {city}", fontsize=14)
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Wind Speed (m/s)', fontsize=12)
            plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)
            plt.legend(loc='upper right')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()

            # Show the wind speed plot
            plt.show()

    conn.close()

def simulate_weather_updates():
    """
    Simulate weather updates for several cities over multiple days.
    """
    for city in CITIES:
        mock_data = generate_mock_weather_data(city)
        store_weather_data(mock_data)
    
    rollup_daily_summary()
    visualize_daily_summary()

if __name__ == "__main__":
    simulate_weather_updates()
