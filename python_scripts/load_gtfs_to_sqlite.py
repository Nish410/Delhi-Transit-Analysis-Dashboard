import sqlite3 
import pandas as pd 
import os 

gtfs_data_folder = '.'

# Name of your SQLite database file
db_name = 'delhi_transit.db'


gtfs_files = {
    'agency.txt': 'agency',
    'calendar.txt': 'calendar',
    'routes.txt': 'routes',
    'stops.txt': 'stops',
    'stop_times.txt': 'stop_times',
    'trips.txt': 'trips',
}

# --- Database Connection ---
try: 
    conn = sqlite3.connect(db_name) 
    cursor = conn.cursor() 
    print(f"Successfully connected to SQLite database: {db_name}") 
except sqlite3.Error as e: 
    print(f"Error connecting to database: {e}") 
    exit() 
# --- Data Loading Function ---
def load_gtfs_file(file_name, table_name):
    file_path = os.path.join(gtfs_data_folder, file_name) 
    if not os.path.exists(file_path):
        print(f"Warning: File not found - {file_path}. Skipping.") 
        return 

    try: 
        df = pd.read_csv(file_path, dtype=str)
        
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Successfully loaded {file_name} into table '{table_name}' with {len(df)} rows.")
    except Exception as e:
        print(f"Error loading {file_name} into table '{table_name}': {e}")

# --- Main Loading Process ---
print("\nStarting GTFS data loading...") 
for file_name, table_name in gtfs_files.items(): 
    load_gtfs_file(file_name, table_name) 


print("\nPerforming basic data type adjustments in SQLite (e.g., converting to INTEGER/REAL)...") # Message for data type conversion.


try: 
    cursor.execute("PRAGMA table_info(stops);") 
    columns = [col[1] for col in cursor.fetchall()] 
    if 'stop_lat' in columns and 'stop_lon' in columns:
        
        cursor.execute("ALTER TABLE stops ADD COLUMN stop_lat_real REAL;")
        cursor.execute("ALTER TABLE stops ADD COLUMN stop_lon_real REAL;")
        cursor.execute("UPDATE stops SET stop_lat_real = CAST(stop_lat AS REAL), stop_lon_real = CAST(stop_lon AS REAL);")
        cursor.execute("ALTER TABLE stops DROP COLUMN stop_lat;")
        cursor.execute("ALTER TABLE stops DROP COLUMN stop_lon;")
        cursor.execute("ALTER TABLE stops RENAME COLUMN stop_lat_real TO stop_lat;")
        cursor.execute("ALTER TABLE stops RENAME COLUMN stop_lon_real TO stop_lon;")
        print("Converted stop_lat and stop_lon to REAL in 'stops' table.")
    else:
        print("stop_lat or stop_lon not found in 'stops' table for conversion.") 
except sqlite3.Error as e: 
    print(f"Error converting stop_lat/lon in 'stops' table: {e}") 


    cursor.execute("PRAGMA table_info(trips);") 
    columns = [col[1] for col in cursor.fetchall()] 
    if 'direction_id' in columns:
       
        test_df = pd.read_sql_query("SELECT DISTINCT direction_id FROM trips WHERE direction_id IS NOT NULL;", conn)
       
        if test_df['direction_id'].astype(str).str.isnumeric().all():
            cursor.execute("ALTER TABLE trips ADD COLUMN direction_id_int INTEGER;")
            cursor.execute("UPDATE trips SET direction_id_int = CAST(direction_id AS INTEGER);")
            cursor.execute("ALTER TABLE trips DROP COLUMN direction_id;")
            cursor.execute("ALTER TABLE trips RENAME COLUMN direction_id_int TO direction_id;")
            print("Converted direction_id to INTEGER in 'trips' table.")
        else: 
            print("direction_id in 'trips' table contains non-numeric values, skipping INTEGER conversion.") 
    else: 
        print("direction_id not found in 'trips' table.") 
except sqlite3.Error as e: 
    print(f"Error converting direction_id in 'trips' table: {e}") 


conn.commit()
conn.close() 
print(f"\nGTFS data loading complete. Database '{db_name}' created/updated.") 
print("You can now use a SQLite browser (like DB Browser for SQLite) to view your data.") 
