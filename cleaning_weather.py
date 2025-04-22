import sqlite3

def clean_existing_data():
    conn = sqlite3.connect("final_project.db")
    cur = conn.cursor()

    # Fetch all rows from Weather2025
    cur.execute("SELECT id, temp_max, temp_min, precipitation, humidity FROM Weather2025")
    rows = cur.fetchall()

    for row in rows:
        id_, temp_max, temp_min, precipitation, humidity = row

        try:
            # Remove units and convert to floats
            clean_max = float(str(temp_max).replace("°F", "").strip())
            clean_min = float(str(temp_min).replace("°F", "").strip())
            clean_precip = float(str(precipitation).replace("mm", "").strip())
            clean_humidity = float(str(humidity).replace("%", "").strip())

            # Update the row with cleaned values
            cur.execute('''
                UPDATE Weather2025
                SET temp_max = ?, temp_min = ?, precipitation = ?, humidity = ?
                WHERE id = ?
            ''', (clean_max, clean_min, clean_precip, clean_humidity, id_))
        
        except Exception as e:
            print(f"❌ Skipping row {id_} due to error: {e}")

    conn.commit()
    conn.close()
    print("✅ All weather records cleaned!")

# Run the cleanup
if __name__ == "__main__":
    clean_existing_data()
