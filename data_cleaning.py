import sqlite3
import pandas as pd
import os

db_name = 'delhi_transit.db'

db_path = os.path.join('.', db_name)

try:
    conn = sqlite3.connect(db_path)
    print(f"Successfully connected to SQLite database: {db_name}")
except sqlite3.Error as e:
    print(f"Error connecting to database: {e}")
    exit()

def load_table_to_df(table_name):
    """Loads a table from SQLite into a Pandas DataFrame."""
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        print(f"Loaded '{table_name}' table into DataFrame with {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        print(f"Error loading table '{table_name}': {e}")
        return None

# Load necessary tables
routes_df = load_table_to_df('routes')
stops_df = load_table_to_df('stops')
trips_df = load_table_to_df('trips')
stop_times_df = load_table_to_df('stop_times')

if any(df is None for df in [routes_df, stops_df, trips_df, stop_times_df]):
    print("One or more essential tables failed to load. Exiting.")
    conn.close()
    exit()

print("\nStarting initial data cleaning and feature engineering...")

def convert_gtfs_time(time_str):
    """Converts GTFS time string (HH:MM:SS, can exceed 23:59:59) to seconds from midnight."""
    if pd.isna(time_str):
        return None
    parts = str(time_str).split(':')
    if len(parts) != 3:
        
        return None
    try:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
        return hours * 3600 + minutes * 60 + seconds
    except ValueError:
        return None 

print("Converting arrival_time and departure_time to seconds from midnight...")
stop_times_df['arrival_time_seconds'] = stop_times_df['arrival_time'].apply(convert_gtfs_time)
stop_times_df['departure_time_seconds'] = stop_times_df['departure_time'].apply(convert_gtfs_time)

if 'arrival_time_seconds' in stop_times_df.columns and 'departure_time_seconds' in stop_times_df.columns:
    stop_times_df = stop_times_df.drop(columns=['arrival_time', 'departure_time'])
    print("Original 'arrival_time' and 'departure_time' columns dropped.")
else:
    print("Warning: Conversion to seconds failed for some time values. Original columns retained.")

print("Calculating scheduled trip durations...")

trip_start_end_times = stop_times_df.groupby('trip_id').agg(
    first_departure_seconds=('departure_time_seconds', 'min'),
    last_arrival_seconds=('arrival_time_seconds', 'max')
).reset_index()

trip_start_end_times['scheduled_duration_seconds'] = (
    trip_start_end_times['last_arrival_seconds'] - trip_start_end_times['first_departure_seconds']
)

trip_start_end_times.loc[trip_start_end_times['scheduled_duration_seconds'] < 0, 'scheduled_duration_seconds'] = pd.NA

trip_start_end_times['scheduled_duration_minutes'] = trip_start_end_times['scheduled_duration_seconds'] / 60

trips_df = pd.merge(trips_df, trip_start_end_times[['trip_id', 'scheduled_duration_minutes']], on='trip_id', how='left')
print("Scheduled trip durations calculated and merged into 'trips_df'.")

print("Merging routes and stops information...")
# Merge trips with routes to get route names
master_df = pd.merge(trips_df, routes_df[['route_id', 'route_long_name', 'route_short_name', 'route_type']], on='route_id', how='left')

print("\nInitial data cleaning and feature engineering complete.")
print("Preview of 'master_df' (trips with route details and scheduled duration):")
print(master_df.head())
print("\nDataFrame Info for 'master_df':")
master_df.info()

print("\nSaving cleaned and enriched data to CSV files...")

output_dir = 'cleaned_data'
os.makedirs(output_dir, exist_ok=True)

master_df.to_csv(os.path.join(output_dir, 'cleaned_master_trips_data.csv'), index=False)
print(f"Saved 'master_df' to {os.path.join(output_dir, 'cleaned_master_trips_data.csv')}")

stop_times_df.to_csv(os.path.join(output_dir, 'cleaned_stop_times_data.csv'), index=False)
print(f"Saved 'stop_times_df' to {os.path.join(output_dir, 'cleaned_stop_times_data.csv')}")

stops_df.to_csv(os.path.join(output_dir, 'cleaned_stops_data.csv'), index=False)
print(f"Saved 'stops_df' to {os.path.join(output_dir, 'cleaned_stops_data.csv')}")

routes_df.to_csv(os.path.join(output_dir, 'cleaned_routes_data.csv'), index=False)
print(f"Saved 'routes_df' to {os.path.join(output_dir, 'cleaned_routes_data.csv')}")

conn.close()
print(f"\nDatabase connection to {db_name} closed.")
