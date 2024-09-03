import requests
import concurrent.futures

# Base URL components
base_url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25_1hr.pl"
dir_param = "%2Fgfs.20240902%2F18%2Fatmos"
file_prefix = "gfs.t18z.pgrb2.0p25.anl"

# Variables and levels
var_VFLX = "on"
var_VIS = "on"
lev_surface = "on"

# Subregion coordinates
toplat = "31.1859"
leftlon = "20.0026"
rightlon = "146.8982"
bottomlat = "-60.0"

# Function to download a file given the forecast hour
def download_file(hour):
    hour_str = f"f{hour:03d}"

    # Construct the full URL with new variables and levels
    full_url = (
        f"{base_url}?dir={dir_param}&file={file_prefix}&"
        f"var_VFLX={var_VFLX}&var_VIS={var_VIS}&lev_surface={lev_surface}&"
        f"toplat={toplat}&leftlon={leftlon}&rightlon={rightlon}&bottomlat={bottomlat}"
    )

    # Send the GET request to download the file
    try:
        response = requests.get(full_url)
    except Exception as e:
        print(f"Error downloading {full_url}: {e}")
        return None

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
            if result:
                print(f"Hour {hour} file downloaded: {result}")

print("All files downloaded successfully.")
