import sqlite3
import requests
from datetime import datetime, timedelta

# Constants
DB_NAME = "final_project.db"
LAT = 42.2808
LON = -83.7430
BATCH_SIZE = 25

# Celsius to Fahrenheit
def c_to_f(c):
    return (c * 9/5) + 32

# Create database
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Weather2024 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT UNIQUE,
            temp_max TEXT,
            temp_min TEXT,
            precipitation TEXT,
            humidity TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Get the next date to fetch
def get_next_start_date():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT MAX(date) FROM Weather2024")
    last_date = cur.fetchone()[0]
    conn.close()

    if last_date:
        next_date = datetime.strptime(last_date, "%Y-%m-%d") + timedelta(days=1)
    else:
        next_date = datetime(2024, 1, 1)
    return next_date

# Fetch daily weather data from Open-Meteo
def fetch_weather_data(start_date, days):
    end_date = start_date + timedelta(days=days - 1)
    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LAT}&longitude={LON}&start_date={start_date.date()}&end_date={end_date.date()}"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_mean"
        f"&timezone=America%2FDetroit"
    )
    response = requests.get(url)
    return response.json()

# Store formatted data
def store_data(data):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    dates = data['daily']['time']
    temps_max = data['daily']['temperature_2m_max']
    temps_min = data['daily']['temperature_2m_min']
    precip = data['daily']['precipitation_sum']
    humidity = data['daily']['relative_humidity_2m_mean']

    for i in range(len(dates)):
        try:
            max_f = f"{round(c_to_f(temps_max[i]), 1)} °F"
            min_f = f"{round(c_to_f(temps_min[i]), 1)} °F"
            precip_mm = f"{precip[i]} mm"
            humidity_pct = f"{humidity[i]} %"

            cur.execute('''
                INSERT INTO Weather2024 (date, temp_max, temp_min, precipitation, humidity)
                VALUES (?, ?, ?, ?, ?)
            ''', (dates[i], max_f, min_f, precip_mm, humidity_pct))

            print(f"✅ Added {dates[i]} → Max: {max_f}, Min: {min_f}, Precip: {precip_mm}, Humidity: {humidity_pct}")
        except sqlite3.IntegrityError:
            print(f"⏭️ Skipped duplicate: {dates[i]}")

    conn.commit()
    conn.close()

# Main function
def main():
    create_db()
    start_date = get_next_start_date()

    if start_date.year != 2024:
        print("🎉 All data for 2024 is already collected!")
        return

    print(f"📆 Collecting data starting from {start_date.date()}...")
    data = fetch_weather_data(start_date, BATCH_SIZE)
    store_data(data)

if __name__ == "__main__":
    main()
