import requests
import pandas as pd
from datetime import datetime

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Latitude ranges
latitude_ranges = [(-90, -60), (-60, -30), (-30, -20), (-20, -10), (-10, 0), (0, 10), (10, 20), (20, 30), (30, 60), (60, 90)]

list_of_years = [1974, 1975, 1976, 1977, 1978, 1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]


# This function processes the data and calculates sunspot lifespans
def retrieve_and_process_data(year):
    url = f"http://fenyi.solarobs.epss.hun-ren.hu/ftp/pub/DPD/data/DPD{year}.txt"
    response = requests.get(url)
    
    if response.status_code == 200:
        content = response.text
        lines = content.splitlines()

        group_dates = {}

        for line in lines:
            if line.startswith('g'):
                columns = line.split()
                group_number = columns[7]
                
                try:
                    group_number = int(group_number)
                except ValueError:
                    continue

                # Get the date and latitude from the row
                date_str = f"{columns[1]}-{columns[2]}-{columns[3]}"
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                latitude = float(columns[12])
                
                if group_number not in group_dates:
                    group_dates[group_number] = {'dates': [], 'latitudes': []}

                group_dates[group_number]['dates'].append(date_obj)
                group_dates[group_number]['latitudes'].append(latitude)
                
        return group_dates
    else:
        print(f"Failed to retrieve data for year {year}")
        return {}

# Calculate the average lifespan of sunspots in each latitude range
def calculate_average_lifespans(group_dates):
    lifespans_by_latitude_range = {r: [] for r in latitude_ranges}
    
    for group, data in group_dates.items():
        if data['dates']:
            # Calculate the lifespan for each sunspot group
            min_date = min(data['dates'])
            max_date = max(data['dates'])
            lifespan = (max_date - min_date).days + 1  # Lifespan in days
            
            # Assign lifespan to latitude range
            avg_latitude = sum(data['latitudes']) / len(data['latitudes'])
            for r in latitude_ranges:
                if r[0] <= avg_latitude < r[1]:
                    lifespans_by_latitude_range[r].append(lifespan)
    
    # Calculate the average lifespan for each range
    avg_lifespans = {r: (sum(lifespans) / len(lifespans)) if lifespans else 0 for r, lifespans in lifespans_by_latitude_range.items()}
    return avg_lifespans

# Main loop to process multiple years
all_group_dates = {}

for year in list_of_years:
    yearly_group_dates = retrieve_and_process_data(year)
    all_group_dates.update(yearly_group_dates)

avg_lifespans = calculate_average_lifespans(all_group_dates)

# Display average lifespans by latitude range
for lat_range, avg_lifespan in avg_lifespans.items():
    print(f"Latitude range {lat_range}: Average lifespan = {avg_lifespan:.2f} days")


# Plot the average lifespan per latitude range using a bar graph
latitude_labels = [f"{r[0]} to {r[1]}" for r in latitude_ranges]
avg_lifespan_values = [avg_lifespans[r] for r in latitude_ranges]

plt.figure(figsize=(10, 6))
plt.bar(latitude_labels, avg_lifespan_values, color='skyblue', edgecolor='black')

# Add labels and title
plt.xlabel('Latitude Range')
plt.ylabel('Average Sunspot Lifespan (Days)')
plt.title('Average Sunspot Lifespan by Latitude Range')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Display the bar graph
plt.tight_layout()
plt.show()