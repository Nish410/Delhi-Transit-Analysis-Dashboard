# Delhi-Transit-Analysis-Dashboard
Interactive data visualization of public transportation system of Delhi utilizing Tableau together with GTFS data.

#Project overview
An interactive data visualization dashboard made in Tableau Public is being proposed. With the analysis of the GTFS feeds for Public Transit services in the city of Delhi, the analysis covers bus routes, stop activity, trip durations, and transit patterns in general. The idea is to have an easy-to-understand interactive application for stakeholders interested in urban mobility and public transportation optimization.

# Project Structure
The repository is organized as follows:
* `cleaned_data/`: This folder contains the cleaned GTFS data files that were used for the analysis:
    * `cleaned_master_trips_data.csv`: Consolidated trip data.
    * `cleaned_stops_data.csv`: Information on the geography and name of a transit stop.
    * `cleaned_routes_data.csv`: (Make sure to mention this file if it is in your `cleaned_data` folder) Information on transit routes.
* `python_scripts/`: This folder contains the Python script(s) used to clean and preprocess the data:
    * `advanced_transit_analysis.py`
    * `data_cleaning.py`
    * `load_gtfs_to_sqlite.py`
 
# Data Source
The raw data for this project is based on the General Transit Feed Specification (GTFS) for Delhi.

# Data Cleaning and Pre-processing
The raw GTFS data was processed in sequence with Python scripts to get the relevant data and clean up what was needed. Specifically, this process:
* Parsed the GTFS `.txt` files (trips.txt, stop_times.txt, stops.txt).
* Joined what was relevant in the tables based on identified keys (trip_id, route_id, stop_id).
* Computed derived metrics: Scheduled Duration Minutes, Scheduled Distance Miles.
* Addressing gaps in values and assuring all data was consistent for visualization.
* The scripts in `python_scripts/` detail the method in complete to clean and prepare the data

# Key Visualizations 
The interactive dashboard provides visualizations that reveal the following : 

1. Transit Stop Locations: A geographical map showing all public transit stops across Delhi.
2. Top 10 Busiest Routes: A bar chart showing all scheduled trips on a route, with busiest routes appearing first indicating the busiest transit corridors.
3. Top 10 Most Active Stops: A bar chart for individual stops indicating the total scheduled stop visits. 
4. Trip Duration Distribution: A histogram indicating total number of trips occurring within various trip duration ranges; indicating common travel times. 
5. Number of Stops per Route: A bar chart for each route indicating the number of unique stops served by each route, indicating how complex the route is.

# Technologies Used
1. Tableau Public: For creating interactive data visualizations and dashboards.
2. Python (using Pandas): For extracting, cleaning, transforming, and preparing the CSV files.
3. SQLite3: For managing databases, and appropriately storing/retrieving processed GTFS data.

# View the Live Dashboard
You can interact with the full dashboard directly on Tableau Public here:
[https://public.tableau.com/app/profile/nisha.saklani/viz/DelhiTransitAnalysisDashboard/PublicTransitOptimisationDashboard]

# How to Use This Project
1. View Live Dashboard: Click the "View the Live Dashboard" link above in order to interact with the Tableau visualizations that are publicly available.
2. Examine the Data: If you want to use the cleaned CSV files for different analysis or projects they will be in the `cleaned_data/` directory.
3. Look at Cleaning Process: If you want to look at the format of the data as well as the actual data transformation, you can find the Python script(s) convert the data files in the `python_scripts/` directory as well as a full SQLite database restore.

Developed By:
Nisha Saklani



