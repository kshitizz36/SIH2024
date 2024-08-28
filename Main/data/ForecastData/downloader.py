import requests
import concurrent.futures

# Base URL components
base_url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl"
dir_param = "%2Fgfs.20240825%2F12%2Fatmos"
file_prefix = "gfs.t12z.pgrb2.0p25."

# Variables and levels
var_UGRD = "on"
var_VGRD = "on"
lev_10_m_above_ground = "on"

# Subregion coordinates
toplat = "31.1859"
leftlon = "20.0026"
rightlon = "146.8982"
bottomlat = "-60.0"

# Function to download a file given the forecast hour
def download_file(hour):
    hour_str = f"f{hour:03d}"

    # Construct the full URL
    full_url = (
        f"{base_url}?dir={dir_param}&file={file_prefix}{hour_str}&"
        f"var_UGRD={var_UGRD}&var_VGRD={var_VGRD}&lev_10_m_above_ground={lev_10_m_above_ground}&"
        f"toplat={toplat}&leftlon={leftlon}&rightlon={rightlon}&bottomlat={bottomlat}"
    )

    # Send the GET request to download the file
    try:
        response = requests.get(full_url)
    except:
        print('retrying for ',full_url)

    # Save the content to a file
    filename = f"tmp/gfs_{hour_str}.grb2"
    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"Downloaded and saved {filename}")
    return filename

# Use ThreadPoolExecutor to download files in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    hours = range(0, 385, 1)  # Hour range from 000 to 384
    # Start the download operations and mark each future with its hour
    futures = {executor.submit(download_file, hour): hour for hour in hours}

    # As each thread completes, print its result
    for future in concurrent.futures.as_completed(futures):
        hour = futures[future]
        try:
            result = future.result()
        except Exception as exc:
            print(f"Hour {hour} generated an exception: {exc}")
        else:
            print(f"Hour {hour} file downloaded: {result}")

print("All files downloaded successfully.")
