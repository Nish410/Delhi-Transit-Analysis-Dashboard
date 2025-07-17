import pandas as pd
import os

cleaned_data_dir = 'cleaned_data'

print(f"Loading cleaned data from '{cleaned_data_dir}' directory...")

try:
    master_df = pd.read_csv(os.path.join(cleaned_data_dir, 'cleaned_master_trips_data.csv'))
    stop_times_df = pd.read_csv(os.path.join(cleaned_data_dir, 'cleaned_stop_times_data.csv'))
    stops_df = pd.read_csv(os.path.join(cleaned_data_dir, 'cleaned_stops_data.csv'))
    routes_df = pd.read_csv(os.path.join(cleaned_data_dir, 'cleaned_routes_data.csv'))
    print("All cleaned DataFrames loaded successfully.")
except FileNotFoundError as e:
    print(f"Error: Could not find cleaned data files. Please ensure '{cleaned_data_dir}' exists and contains the CSVs.")
    print(f"Detail: {e}")
    exit()
except Exception as e:
    print(f"An unexpected error occurred while loading cleaned data: {e}")
    exit()

print("\nStarting advanced data analysis and preparation for visualization...")

stop_times_df['arrival_time_seconds'] = pd.to_numeric(stop_times_df['arrival_time_seconds'], errors='coerce')

if 'arrival_time_seconds' in stop_times_df.columns:
    print("Extracting hour of day from arrival times...")
    stop_times_df['arrival_hour'] = (stop_times_df['arrival_time_seconds'] // 3600) % 24
    
    hourly_activity = stop_times_df.groupby('arrival_hour').agg(
        total_stops=('trip_id', 'count') 
    ).reset_index()
    
    print("\nHourly Activity (Total Stops):")
    print(hourly_activity.sort_values(by='arrival_hour')) 

if 'route_type' in routes_df.columns:
    print("\nAnalyzing Route Types...")
   
    route_type_counts = routes_df['route_type'].value_counts().reset_index()
    route_type_counts.columns = ['route_type', 'count_of_routes']
    print("\nRoute Type Counts (Raw):")
    print(route_type_counts)

    route_type_mapping = {
        '0': 'Tram/Light Rail',
        '1': 'Subway/Metro',
        '2': 'Rail',
        '3': 'Bus',
        '4': 'Ferry',
        '5': 'Cable Car',
        '6': 'Gondola',
        '7': 'Funicular'
    }

    routes_df['route_type_name'] = routes_df['route_type'].astype(str).map(route_type_mapping).fillna('Other')
    print("Mapped route_type codes to names in 'routes_df'.")

    if 'route_type_name' not in master_df.columns:
         master_df = pd.merge(master_df, routes_df[['route_id', 'route_type_name']], on='route_id', how='left')
         print("Route type names merged into 'master_df'.")

    master_df['scheduled_duration_minutes'] = pd.to_numeric(master_df['scheduled_duration_minutes'], errors='coerce')
    avg_duration_by_type = master_df.groupby('route_type_name')['scheduled_duration_minutes'].mean().reset_index()
    print("\nAverage Scheduled Trip Duration by Route Type:")
    print(avg_duration_by_type)
else:
    print("\n'route_type' column not found in routes_df. Skipping route type analysis.")


# Top 10 Busiest Routes (from master_df)
print("\nTop 10 Busiest Routes (from master_df):")
busiest_routes_df = master_df.groupby(['route_id', 'route_long_name']).agg(
    total_trips=('trip_id', 'count')
).reset_index()
print(busiest_routes_df.sort_values(by='total_trips', ascending=False).head(10))

# Top 10 Most Active Stops (from stop_times_df)
print("\nTop 10 Most Active Stops (from stop_times_df):")
stop_times_with_names_df = pd.merge(stop_times_df, stops_df[['stop_id', 'stop_name']], on='stop_id', how='left')
most_active_stops_df = stop_times_with_names_df.groupby(['stop_id', 'stop_name']).agg(
    total_stop_visits=('trip_id', 'count')
).reset_index()
print(most_active_stops_df.sort_values(by='total_stop_visits', ascending=False).head(10))

print("\nReady for Power BI visualization using the CSVs in 'cleaned_data' folder.")
