import sqlite3
from datetime import datetime, timedelta
import random

def inject_history():
    conn = sqlite3.connect('clinic.db')
    cursor = conn.cursor()
    
    # Get all patients
    cursor.execute("SELECT id FROM patients")
    patients = cursor.fetchall()
    
    if not patients:
        print("No patients found.")
        return

    print(f"Found {len(patients)} patients. Distributing history...")
    
    # Keep 40% in Today
    # Move 30% to Last 7 Days (Random)
    # Move 30% to Last 30 Days (Random)
    
    count_week = 0
    count_month = 0
    
    for row in patients:
        pid = row[0]
        choice = random.random()
        
        new_date = None
        
        if choice < 0.4:
            # Keep today (do nothing)
            continue
        elif choice < 0.7:
            # Last 7 days
            days_ago = random.randint(1, 6)
            new_date = datetime.now() - timedelta(days=days_ago)
            count_week += 1
        else:
            # Last 30 days
            days_ago = random.randint(7, 29)
            new_date = datetime.now() - timedelta(days=days_ago)
            count_month += 1
            
        if new_date:
            # Randomize time too
            rand_hour = random.randint(9, 17) # 9 AM to 5 PM
            rand_min = random.randint(0, 59)
            new_date = new_date.replace(hour=rand_hour, minute=rand_min)
            
            timestamp = new_date.strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("UPDATE patients SET created_at = ? WHERE id = ?", (timestamp, pid))
            
    conn.commit()
    conn.close()
    print(f"Update Complete: {count_week} moved to previous week, {count_month} moved to previous month.")

if __name__ == "__main__":
    inject_history()
