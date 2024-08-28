import pygrib

# Open the GRIB file
grib_file = 'ForecastData/tmp/gfs.t12z.pgrb2.0p25.f000'


grbs = pygrib.open(grib_file)

# Print the contents of the GRIB file
for grb in grbs:
    print(f"Parameter Name: {grb.name}")
    print(f"Short Name: {grb.shortName}")
    print(f"Type of Level: {grb.typeOfLevel}")
    print(f"Level: {grb.level}")
    print(f"Forecast Time: {grb.forecastTime} hours")
    print(f"Valid Date: {grb.validDate}")
    print(f"Anal Date: {grb.analDate}")
    print(f"Units: {grb.units}")
    print('-' * 50)
    print(grb.data_values)
    print('-' * 50)


# Close the file
grbs.close()
