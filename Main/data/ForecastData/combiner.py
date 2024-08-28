import pygrib

# Path to the combined GRIB2 file
grib_file = 'combined_output.grb2'

# Open the GRIB2 file
grbs = pygrib.open(grib_file)

# Loop over each message and print out the details
for grb in grbs:
    print(f"Parameter Name: {grb.name}")
    print(f"Short Name: {grb.shortName}")
    print(f"Type of Level: {grb.typeOfLevel}")
    print(f"Level: {grb.level}")
    print(f"Forecast Time: {grb.forecastTime} hours")
    print(f"Valid Date: {grb.validDate}")
    print(f"Anal Date: {grb.analDate}")
    print(f"Units: {grb.units}")
    
    # Get the data values (printing a small sample)
    data_values = grb.values
    print(f"Data (sample): {data_values[:5, :5]}")
    
    # Get the corresponding latitudes and longitudes (printing a small sample)
    lats, lons = grb.latlons()
    print(f"Latitudes (sample): {lats[:5, :5]}")
    print(f"Longitudes (sample): {lons[:5, :5]}")
    
    print('-' * 50)

grbs.close()
